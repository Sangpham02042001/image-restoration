from timeit import default_timer as timer

import cv2
import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from enhancer.models.MPRNet_denoise import MPRNetDenoise
from enhancer.models.MPRNet_deblur import MPRNetDeblur
from enhancer.models.network_swinir import SwinIR
from enhancer.resources.const import DEBLUR_MODEL_PATH, DENOISE_MODEL_PATH, SR_MODEL_PATH
from skimage import img_as_ubyte
from enhancer.utils import load_checkpoint


class ImageEnhancer:
    def __init__(self):
        pass

    def enhance(self, img):
        img_tensor = TF.to_tensor(img)

        img_tensor = img_tensor.unsqueeze(0).cuda()

        factor = 8
        h, w = img_tensor.shape[2], img_tensor.shape[3]
        H, W = ((h + factor) // factor) * factor, ((w + factor) // factor) * factor

        padh = H - h if h % factor != 0 else 0
        padw = W - w if w % factor != 0 else 0

        input_padded = F.pad(img_tensor, (0, padw, 0, padh), "reflect")
        with torch.no_grad():
            output = self.model_restoration(input_padded)
            if type(output) == list:
                output = output[0]
        output = torch.clamp(output, 0, 1)

        # output = output[:, :, :h, :w]
        output = output.permute(0, 2, 3, 1)[0].cpu().detach().numpy()
        output_img = img_as_ubyte(output)

        return output_img


class Deblurrer(ImageEnhancer):
    def __init__(self):
        super(Deblurrer, self).__init__()

        self.model_restoration = MPRNetDeblur().cuda()
        load_checkpoint(self.model_restoration, DEBLUR_MODEL_PATH)

        self.model_restoration.eval()


class Denoiser(ImageEnhancer):
    def __init__(self):
        super(Denoiser, self).__init__()

        self.model_restoration = MPRNetDenoise().cuda()
        load_checkpoint(self.model_restoration, DENOISE_MODEL_PATH)

        self.model_restoration.eval()


class SuperResolver(ImageEnhancer):
    def __init__(self):
        param_key_g = 'params_ema'
        self.model_restoration = SwinIR(upscale=4, in_chans=3, img_size=64, window_size=8,
                                        img_range=1., depths=[6, 6, 6, 6, 6, 6], embed_dim=180, num_heads=[6, 6, 6, 6, 6, 6],
                                        mlp_ratio=2, upsampler='nearest+conv', resi_connection='1conv').cuda()

        pretrained_model = torch.load(SR_MODEL_PATH)
        self.model_restoration.load_state_dict(pretrained_model[param_key_g] if param_key_g in pretrained_model.keys() else pretrained_model, strict=True)

        self.model_restoration.eval()


if __name__ == "__main__":
    deblurrer = Denoiser()

    start = timer()
    img_enhanced = deblurrer.enhance("enhancer/imgs/test_denoise.png")
    end = timer()

    print(end - start)

    cv2.imwrite("enhancerimgs/test_denoise_enhanced.png", cv2.cvtColor(img_enhanced, cv2.COLOR_RGB2BGR))
