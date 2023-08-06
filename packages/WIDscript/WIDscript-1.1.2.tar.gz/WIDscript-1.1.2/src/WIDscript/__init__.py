 
#  I8,        8        ,8I  88  88888888ba,      ,ad8888ba,   I8,        8        ,8I  888b      88
#  `8b       d8b       d8'  88  88      `"8b    d8"'    `"8b  `8b       d8b       d8'  8888b     88
#   "8,     ,8"8,     ,8"   88  88        `8b  d8'        `8b  "8,     ,8"8,     ,8"   88 `8b    88
#    Y8     8P Y8     8P    88  88         88  88          88   Y8     8P Y8     8P    88  `8b   88
#    `8b   d8' `8b   d8'    88  88         88  88          88   `8b   d8' `8b   d8'    88   `8b  88
#     `8a a8'   `8a a8'     88  88         8P  Y8,        ,8P    `8a a8'   `8a a8'     88    `8b 88
#      `8a8'     `8a8'      88  88      .a8P    Y8a.    .a8P      `8a8'     `8a8'      88     `8888
#       `8'       `8'       88  88888888Y"'      `"Y8888Y"'        `8'       `8'       88      `888

# Only content downloaded from the official WIDOWN website originates solely from us.
# If you have acquired this content from any other source, it may not be genuine.
# It could have been "stolen" or someone could be impersonating us.

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# WIDscript

from    enum           import Enum

from    vapoursynth    import core
import  vapoursynth    as vs

core = vs.core

from    vskernels      import Hermite, BSpline, Mitchell
from    dfttest2       import DFTTest
from    havsfunc       import DeHalo_alpha, HQDeringmod
from    kagefunc       import retinex_edgemask
from    vsmasktools    import retinex
from    vsdpir_ncnn    import DPIR
from    vsTAAmbk       import TAAmbk
from    vsscale        import SSIM
from    vstools        import finalize_clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

class cFormatEnum(str, Enum):
    YUV420P10 = "YUV420P10",
    YUV420P16 = "YUV420P16",
    RGBS      = "RGBS"
    
############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def format(clip    : vs.VideoNode,
           cFormat : cFormatEnum = cFormatEnum.YUV420P16) :
        
    match cFormat :
        case "YUV420P10":
            if (clip.format.name != cFormatEnum.YUV420P10) : clip = core.resize.Spline36(clip, format=vs.YUV420P10, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")
        case "YUV420P16":
            if (clip.format.name != cFormatEnum.YUV420P16) : clip = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")
        case "RGBS":
            if (clip.format.name != cFormatEnum.RGBS)      : clip = core.resize.Spline36(clip, format=vs.RGBS, matrix_in_s="709", dither_type="error_diffusion")
        case _:
            raise ValueError("Invalid value")
                 
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def initClip(clip,
             isInterlaced  : bool = False,
             setResolution : bool = False,
             siWidth       : int  = 704,
             siHeight      : int  = 480,
             fps           : int  = 24000,
             floatFPS      : bool = True) :
    
    # Importing the video
    clip = core.lsmas.LWLibavSource(clip)
    
    if (isInterlaced == True) :
        
        #Restores Progressive Frames
        clip = core.vivtc.VFM(clip, order=1, cthresh=10)

        #Restores framerate to 23.976fps from 29.97fps by removing duplicate frames.
        clip = core.vivtc.VDecimate(clip)
        
    if (setResolution == True) :
        
        # Changes Aspect Ratio to Fullscreen
        clip = clip.resize.Spline36(siWidth, siHeight, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")
        
    # Verifying whether FPS are float or not, in order to then define the FPS of the source.
    clip = clip.std.AssumeFPS(fpsnum=fps, fpsden=1001) if (floatFPS == True) else clip.std.AssumeFPS(fpsnum=fps)

    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def spliceClip(clip               : vs.VideoNode,
                source            : vs.VideoNode,
                parameters_slice  : dict = None,
                useInOut          : bool = False,
                inOutPath         : str  = None) :
    
    start, end = parameters_slice['start'], parameters_slice['end'] + 2
    if (start == None or end == None or end == 1) : raise ValueError("'None' isn't a valid value !")
    
    parameters_slice = {**parameters_slice, 'end': end}

    if (useInOut == True and inOutPath == None)   : raise ValueError("'None' isn't a valid path !")
    
    slice = everything(source, **parameters_slice) if (useInOut == False) else initClip(inOutPath)
    clip  = core.std.Splice([clip[:start], slice, clip[end:]])
    
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def hdr2SDR(clip    : vs.VideoNode,
            dst_max : int   = 110,
            src_max : int   = 4000,
            src_min : float = 0.0050) :
    
    clip = format(clip)
    clip = core.placebo.Tonemap(clip, src_csp=1, dst_csp=0, dst_prim=3, dynamic_peak_detection=1, dst_max=dst_max, src_max=src_max, src_min=src_min, tone_mapping_function=6, tone_mapping_mode=4, gamut_mode=0)
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def downscale(clip     : vs.VideoNode,
              dsWidth  : int = 1920,
              dsHeight : int = 1080) :

    clip = format(clip)
    clip = SSIM.scale(clip, dsWidth, dsHeight)
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def mage(clip             : vs.VideoNode,
         thsxdxMultiplier : float = 0.65) :

    """## MAGE - Managing All Grain Elegantly, made by Clybius and modified by WIDOWN.
    
    The "MAGE" function aims to fix any issues present in the original video clip such as agressive noise, while preserving details and improving sharpness.\n
    It is recommended to use it for anim-type content because otherwise, it can create "wrapping" effects, similar to those caused by AI video interpolation.
    
    """

    clip = format(clip)

    # all levels for MAnalyse
    super = core.mv.Super(clip, hpad=32, vpad=32, rfilter=4)

    # Truemotion for max denoising on original vid
    backward2 = core.mv.Analyse(super, isb=True, blksize=32, overlap=16, delta=2, search=5, truemotion=True)
    backward  = core.mv.Analyse(super, isb=True, blksize=32, overlap=16, search=5, truemotion=True)
    forward   = core.mv.Analyse(super, isb=False, blksize=32, overlap=16, search=5, truemotion=True)
    forward2  = core.mv.Analyse(super, isb=False, blksize=32, overlap=16, search=5, delta=2, truemotion=True)

    dn1 = core.mv.Degrain2(clip, super, backward, forward, backward2, forward2, thsad=int(200*thsxdxMultiplier), thscd1=int(220*thsxdxMultiplier), thscd2=int(105*thsxdxMultiplier), plane=0) # Heavily denoise for edge mask
    
    # Sharpen clip for non-shown motion compensated frames, helps
    # retain higher frequency detail at the expense of denoise strength.
    compSharp = core.cas.CAS(dn1, sharpness=1)

    # all levels for MAnalyse
    superdn1   = core.mv.Super(dn1, hpad=32, vpad=32, rfilter=4)
    superSharp = core.mv.Super(compSharp, hpad=32, vpad=32, rfilter=4)

    # Calculate new mvs using new denoised clip, truemotion off for detail retention
    backward2 = core.mv.Analyse(superdn1, isb=True, blksize=32, overlap=16, delta=2, truemotion=False, trymany=True)
    backward  = core.mv.Analyse(superdn1, isb=True, blksize=32, overlap=16, truemotion=False, trymany=True)
    forward   = core.mv.Analyse(superdn1, isb=False, blksize=32, overlap=16, truemotion=False, trymany=True)
    forward2  = core.mv.Analyse(superdn1, isb=False, blksize=32, overlap=16, delta=2, truemotion=False, trymany=True)

    # Recalculate bad mvs with truemotion on to ensure a motion vector is used in denoising
    backward2 = core.mv.Recalculate(superdn1, backward2, blksize=8, overlap=4, search=3, searchparam=4, dct=6, truemotion=True) 
    backward  = core.mv.Recalculate(superdn1, backward, blksize=8, overlap=4, search=3, searchparam=4, dct=6, truemotion=True)
    forward   = core.mv.Recalculate(superdn1, forward, blksize=8, overlap=4, search=3, searchparam=4, dct=6, truemotion=True)
    forward2  = core.mv.Recalculate(superdn1, forward2, blksize=8, overlap=4, search=3, searchparam=4, dct=6, truemotion=True)

    backward_re2 = core.mv.Finest(backward2)
    backward_re  = core.mv.Finest(backward)
    forward_re   = core.mv.Finest(forward)
    forward_re2  = core.mv.Finest(forward2)

    clipDN = core.mv.Degrain2(clip, superSharp, backward_re, forward_re, backward_re2, forward_re2, thsad=int(200*thsxdxMultiplier), thscd1=int(220*thsxdxMultiplier), thscd2=int(105*thsxdxMultiplier))

    # Get Y plane.
    clipPre = core.std.ShufflePlanes(clipDN, planes=0, colorfamily=vs.GRAY)

    # Retinex for better masking.
    dmask = retinex(clipPre, sigma=[50, 200, 350], upper_thr=0.002, lower_thr=0.01)

    # This mask can be changed, suitable for IRL content due to the minimum and then increasing the strength in levels,
    # thus increasing the mask strength while not binarizing (pure black/pure white) the mask or adding miniscule detail.
    dmask = core.tcanny.TCanny(dmask, mode=1, op=1, scale=1.2).std.Levels(min_in=4000, gamma=4.0)

    # Take original clip, and apply it on top of the denoised clip via the mask.
    clipDN = core.std.MaskedMerge(clipDN, clip, dmask, planes=0)

    # 2nd pass light denoise, lower or raise `sigma` for lower or higher strength.
    clipDN = DFTTest(clipDN, sigma=0.9, tbsize=3, ssystem=1)

    # Bicubic Spline Desharpening
    clipDNS  = clipDN
    
    clipDNSU = Hermite().scale(clipDNS, clipDN.width * 1.5, clipDN.height * 1.5)
    clipDNU  = BSpline().scale(clipDN, clipDN.width * 1.5, clipDN.height * 1.5)
    
    clipDNS  = core.std.MakeDiff(clipDNU, clipDNSU)
    
    clipDNS  = Mitchell().scale(clipDNS, clipDN.width, clipDN.height)
    
    clipDN   = core.std.MergeDiff(clipDN, clipDNS)
    # Bicubic Spline Desharpening
    
    return clipDN

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def upscale(clip          : vs.VideoNode,
            isAnime       : bool = True,
            fsrcnnxPath   : str  = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1.glsl",
            fsrcnnxLaPath : str  = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1_LineArt.glsl",
            usWidth       : int  = 1920,
            usHeight      : int  = 1080) :
    
    # Verifying which upcaling model should be used depending on the content.
    fsrcnnxFinalPath = fsrcnnxLaPath if (isAnime == True) else fsrcnnxPath
    
    clip = format(clip)
    clip = core.placebo.Shader(clip, fsrcnnxFinalPath,  usWidth, usHeight, filter="catmull_rom", antiring=0.7)
    return clip
    
############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def dehalo(clip : vs.VideoNode) :
    clip = format(clip)
    clip = DeHalo_alpha(clip, darkstr=0.4)
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    
def dering(clip : vs.VideoNode) :
    clip = format(clip)
    clip = HQDeringmod(clip, mrad=8, nrmode=0, darkthr=True)
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def aa(clip    : vs.VideoNode,
       useUsAA : bool = True) :
    
    clip = format(clip)
    clip = TAAmbk(clip, aatype='Nnedi3UpscaleSangNom', opencl=True) if (useUsAA == True) else TAAmbk(clip, aatype='Eedi3', opencl=True)
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def dpir(clip                   : vs.VideoNode,
         dpirTileDenominator    : int  = 2,
         dpirDeblocking         : bool = True,
         dpirDenoising          : bool = True,
         dpirDeblockingStrength : int  = 15,
         dpirDenoisingStrength  : int  = 1) :
    
    clip = format(clip, cFormatEnum.RGBS)

    # Divide frames by tiles to save on VRAM.
    dpirTileW = int(clip.width  / dpirTileDenominator)
    dpirTileH = int(clip.height / dpirTileDenominator)

    # AI Assisted deblocking & denoising.
    if (dpirDeblocking == True) : clip = DPIR(task='deblock').run(clip, strength=dpirDeblockingStrength, tile_w=dpirTileW, tile_h=dpirTileH)
    if (dpirDenoising  == True) : clip = DPIR(task='denoise').run(clip, strength=dpirDenoisingStrength,  tile_w=dpirTileW, tile_h=dpirTileH)
    
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def deband(clip          : vs.VideoNode,
           dbRemBinarize : int = 1500) :

    clip_edge = format(clip)

    # Creating a retinex edge mask before applying debanding to keep fine details.
    mask = retinex_edgemask(clip_edge).std.Binarize(dbRemBinarize).std.Inflate()

    clip = format(clip, cFormatEnum.RGBS)
    clip = core.placebo.Deband(clip, planes = 1 | 2 | 4, iterations=4, radius=8, threshold=8, grain=6, dither = True, dither_algo = 0)
    clip = format(clip)

    # # Take the edge clip, and apply it on top of the debanded clip via the mask.
    clip = core.std.MaskedMerge(clip, clip_edge, mask)

    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def finalize(clip: vs.VideoNode) :
    clip = format(clip, cFormatEnum.YUV420P10)
    clip = finalize_clip(clip)
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def everything(clip                   : vs.VideoNode,
               #
               slice                  : bool  = False,
               start                  : int   = 0,
               end                    : int   = 0,
               #
               useHDR2SDR             : bool  = False,
               dst_max                : int   = 110,
               src_max                : int   = 4000,
               src_min                : float = 0.0050,
               #
               useDownscaling         : bool  = False,
               dsWidth                : int   = 1920,
               dsHeight               : int   = 1080,
               #
               useMAGE                : bool  = False,
               thsxdxMultiplier       : float = 0.65,
               #
               useUpscaling           : bool  = False,
               isAnime                : bool  = True,
               fsrcnnxPath            : str   = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1.glsl",
               fsrcnnxLaPath          : str   = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1_LineArt.glsl",
               usWidth                : int   = 1920,
               usHeight               : int   = 1080,
               #
               useDehaloing           : bool  = True,
               useDeringing           : bool  = True,
               useAA                  : bool  = True,
               useUsAA                : bool  = True,
               #
               useDPIR                : bool  = False,
               dpirTileDenominator    : int   = 2,
               dpirDeblocking         : bool  = True,
               dpirDenoising          : bool  = True,
               dpirDeblockingStrength : int   = 15,
               dpirDenoisingStrength  : int   = 1,
               #
               useDebanding           : bool  = False,
               dbRemBinarize          : int   = 1500,
               #
               useFinalizing          : bool  = True) :
    
    if (slice          == True) : clip = clip[start:end]
    if (useHDR2SDR     == True) : clip = hdr2SDR(clip, dst_max, src_max, src_min)
    if (useDownscaling == True) : clip = downscale(clip, dsWidth, dsHeight)
    if (useMAGE        == True) : clip = mage(clip, thsxdxMultiplier)
    if (useUpscaling   == True) : clip = upscale(clip, isAnime, fsrcnnxPath, fsrcnnxLaPath, usWidth, usHeight)
    if (useDehaloing   == True) : clip = dehalo(clip)
    if (useDeringing   == True) : clip = dering(clip)
    if (useAA          == True) : clip = aa(clip, useUsAA)
    if (useDPIR        == True) : clip = dpir(clip, dpirTileDenominator, dpirDeblocking, dpirDenoising, dpirDeblockingStrength, dpirDenoisingStrength)
    if (useDebanding   == True) : clip = deband(clip, dbRemBinarize)
    if (useFinalizing  == True) : clip = finalize(clip)
    
    return clip