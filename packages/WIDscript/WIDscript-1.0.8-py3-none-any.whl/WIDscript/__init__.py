 
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

from    vapoursynth    import core
import  vapoursynth    as vs

core = vs.core

from    vskernels      import Hermite, BSpline, Mitchell
from    dfttest2       import DFTTest, Backend
from    denoiseMC      import denoiseMC
from    havsfunc       import SMDegrain, DeHalo_alpha, HQDeringmod
from    kagefunc       import retinex_edgemask
from    vsmasktools    import retinex
from    vsdpir_ncnn    import DPIR
from    vsTAAmbk       import TAAmbk
from    vsscale        import SSIM
from    vstools        import finalize_clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def initClip(clip,
             fps      : int  = 24000,
             floatFPS : bool = True) :
             
    # Importing the video
    clip = core.lsmas.LWLibavSource(clip)

    # Verifying whether FPS are float or not, in order to then define the FPS of the source.
    clip = clip.std.AssumeFPS(fpsnum=fps, fpsden=1001) if (floatFPS == True) else clip.std.AssumeFPS(fpsnum=fps)

    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def splice_clip(clip              : vs.VideoNode,
                source            : vs.VideoNode,
                parameters_slice,
                useInOut          : bool = False,
                inOutPath                = None) :
    
    slice         = everything(source, **parameters_slice) if (useInOut == False) else initClip(inOutPath)
    
    start, end    = parameters_slice['start'], parameters_slice['end']
    
    clip          = core.std.Splice([clip[:start], slice, clip[end:]])
    
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def downscale(clip     : vs.VideoNode,
              dsWidth  : int = 1920,
              dsHeight : int = 1080) :

    clip = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # Downscaling using high quality algo.
    clip = SSIM.scale(clip, dsWidth, dsHeight)

    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def hdr2SDR(clip    : vs.VideoNode,
            dst_max : int   = 110,
            src_max : int   = 4000,
            src_min : float = 0.0050) :
    
    clip = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # Tonemapping for HDR to SDR. Change src_max and src_min according to the source.
    clip = core.placebo.Tonemap(clip, src_csp=1, dst_csp=0, dst_prim=3, dynamic_peak_detection=1, dst_max=dst_max, src_max=src_max, src_min=src_min, tone_mapping_function=6, tone_mapping_mode=4, gamut_mode=0)

    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def mage(clip             : vs.VideoNode,
         thsxdxMultiplier : float = 0.65) :

    # The "MAGE" function aims to fix any issues present in the original video clip such as agressive noise, while preserving details and improving sharpness.

    # Defining a YUV420P16 variable for further filtering with MAGE script.
    clip = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

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
    clipDNS = clipDN # Copy clip

    clipDNSU = Hermite().scale(clipDNS, clipDN.width * 1.5, clipDN.height * 1.5) # Resize using hermite bicubic (0,1)
    clipDNU  = BSpline().scale(clipDN, clipDN.width * 1.5, clipDN.height * 1.5) # Base bspline (0,0)

    clipDNS = core.std.MakeDiff(clipDNU, clipDNSU) # Make diff of the two
    clipDNS = Mitchell().scale(clipDNS, clipDN.width, clipDN.height) # Scale down using "natural" bicubic (0.333, 0.333)

    clipDN = core.std.MergeDiff(clipDN, clipDNS) # Finally, merge together

    return clipDN

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def ddn(clip           : vs.VideoNode,
        bm3dSigma      : float = 0.3,
        ddnRemBinarize : int   = 500,
        smdThSAD       : int   = 250) :
    
    # WARNING : OUTDATED.
    
    # The "DDN" function is designed to enhance the quality of a video clip by addressing common issues such as noise and banding.
    
    clip_YUV420P16 = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # Defining motion compensated denoising.
    def denoised_dft(clip_YUV420P16) :
        return DFTTest(clip_YUV420P16, sigma=8, backend=Backend.CPU, tbsize=5)

    # First pass denoising using denoiseMC, then converting to RGBS for BM3D.
    _1p_denoising = denoiseMC(clip_YUV420P16, radius=5, denoise_fn=denoised_dft)
    _1p_denoising = core.resize.Spline36(_1p_denoising, format=vs.RGBS, matrix_in_s="709", dither_type="error_diffusion")

    # Denoising using BM3D to create a denoised edge clip, using the first pass denoising as ref, then converting to YUV420P16.
    denoised_edgeclip = core.resize.Spline36(clip, format=vs.RGBS, matrix_in_s="709", dither_type="error_diffusion")
    denoised_edgeclip = core.bm3dcpu.BM3D(denoised_edgeclip, ref=_1p_denoising, sigma=bm3dSigma, chroma=False)
    denoised_edgeclip = core.resize.Spline36(denoised_edgeclip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # Creating a retinex edge mask before applying SMDegrain to keep fine details.
    mask = retinex_edgemask(denoised_edgeclip).std.Binarize(ddnRemBinarize).std.Inflate()

    # Second pass denoising using BM3D on the first pass denoising, then converting to YUV420P16 for the third pass.
    _2p_denoising = core.bm3dcpu.BM3D(_1p_denoising, sigma=bm3dSigma, chroma=False)
    _2p_denoising = core.resize.Spline36(_2p_denoising, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # Third pass denoising using SMDegrain on the second pass denoising.
    _3p_denoising = SMDegrain(_2p_denoising, tr=1, pel=2, Str=1.1, contrasharp=True, RefineMotion=True, thSAD=smdThSAD, chroma=False, plane=0, search=3, blksize=16, overlap=8, hpad=16, vpad=16)

    # Take the denoised edge clip, and apply it on top of the debanded clip via the mask.
    ddn_final = core.std.MaskedMerge(_3p_denoising, denoised_edgeclip, mask)

    return ddn_final

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def upscale(clip          : vs.VideoNode,
            isAnime       : bool = True,
            fsrcnnxPath   : str  = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1.glsl",
            fsrcnnxLaPath : str  = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1_LineArt.glsl",
            usWidth       : int  = 1920,
            usHeight      : int  = 1080) :
    
    # Verifying which upcaling model should be used depending on the content.
    fsrcnnxFinalPath = fsrcnnxLaPath if (isAnime == True) else fsrcnnxPath

    #Defining a YUV420P16 variable for more accuracy.
    clip = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # Upscaling using high quality algo.
    clip = core.placebo.Shader(clip, fsrcnnxFinalPath,  usWidth, usHeight, filter="catmull_rom", antiring=0.7)
    
############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def edgeHealing(clip         : vs.VideoNode,
                useDehaloing : bool = True,
                useDeringing : bool = True,
                useAA        : bool = True,
                useUsAA      : bool = True) :
    
    #Defining a YUV420P16 variable for more accuracy.
    clip = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")
    
    # Dehalo & Dering edges.
    if (useDehaloing == True) : clip = DeHalo_alpha(clip, darkstr=0.4)
    if (useDeringing == True) : clip = HQDeringmod(clip, mrad=8, nrmode=0, darkthr=True)

    # If AA is enabled, will then check if upscaling based AA should be used or not. CAUTION : Upscaled based one will destroy grain pattern.
    if (useAA == True) : clip = TAAmbk(clip, aatype='Nnedi3UpscaleSangNom', opencl=True) if (useUsAA == True) else TAAmbk(clip, aatype='Eedi3', opencl=True)

    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def dpir(clip                   : vs.VideoNode,
         dpirTileDenominator    : int  = 2,
         dpirDeblocking         : bool = True,
         dpirDenoising          : bool = True,
         dpirDeblockingStrength : int  = 15,
         dpirDenoisingStrength  : int  = 1) :
    
    # Defining a RGBS variable because its needed before using DPIR.
    clip = core.resize.Spline36(clip, format=vs.RGBS, matrix_in_s="709", dither_type="error_diffusion")

    # Divide frames by tiles to save on VRAM.
    dpirTileW = int(clip.width  / dpirTileDenominator)
    dpirTileH = int(clip.height / dpirTileDenominator)

    # AI Assisted deblocking & denoising.
    if (dpirDeblocking == True) : clip = DPIR(task='deblock').run(clip, strength=dpirDeblockingStrength, tile_w=dpirTileW, tile_h=dpirTileH)
    if (dpirDenoising == True)  : clip = DPIR(task='denoise').run(clip, strength=dpirDenoisingStrength,  tile_w=dpirTileW, tile_h=dpirTileH)
    
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def deband(clip          : vs.VideoNode,
           dbRemBinarize : int = 1500) :

    clip_edge = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # Creating a retinex edge mask before applying SMDegrain to keep fine details.
    mask = retinex_edgemask(clip_edge).std.Binarize(dbRemBinarize).std.Inflate()

    # Debanding using placebo.Deband on the third pass denoising on all planes, then converting to YUV420P16 for the final merging.
    clip = core.resize.Spline36(clip, format=vs.RGBS, matrix_in_s="709", dither_type="error_diffusion")
    clip = core.placebo.Deband(clip, planes = 1 | 2 | 4, iterations=4, radius=8, threshold=8, grain=6, dither = True, dither_algo = 0)
    clip = core.resize.Spline36(clip, format=vs.YUV420P16, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")

    # # Take the denoised edge clip, and apply it on top of the debanded clip via the mask.
    clip = core.std.MaskedMerge(clip, clip_edge, mask)

    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def finalize(clip: vs.VideoNode) :
    # Defining a YUV420P10 variable from the final of the filtering chain, before finalizing and exporting it.
    clip = core.resize.Spline36(clip, format=vs.YUV420P10, matrix_s="709", matrix_in_s="709", dither_type="error_diffusion")
    clip = finalize_clip(clip)
    return clip

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

def everything(clip                   : vs.VideoNode,
               #
               slice                  : bool  = False,
               start                  : int   = 0,
               end                    : int   = 0,
               #
               useDownscaling         : bool  = False,
               dsWidth                : int   = 1920,
               dsHeight               : int   = 1080,
               #
               useHDR2SDR             : bool  = False,
               dst_max                : int   = 110,
               src_max                : int   = 4000,
               src_min                : float = 0.0050,
               #
               useMAGE                : bool  = False,
               thsxdxMultiplier       : float = 0.65,
               #
               useDDN                 : bool  = False,
               bm3dSigma              : float = 0.3,
               ddnRemBinarize         : int   = 500,
               smdThSAD               : int   = 250,
               #
               useUpscaling           : bool  = False,
               isAnime                : bool  = True,
               fsrcnnxPath            : str   = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1.glsl",
               fsrcnnxLaPath          : str   = "C:/Softwares/AV1AN/FSRCNNX_x2_8-0-4-1_LineArt.glsl",
               usWidth                : int   = 1920,
               usHeight               : int   = 1080,
               #
               useEdgeHealing         : bool  = False,
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
    if (useDownscaling == True) : clip = downscale(clip, dsWidth, dsHeight)
    if (useHDR2SDR     == True) : clip = hdr2SDR(clip, dst_max, src_max, src_min)
    if (useMAGE        == True) : clip = mage(clip, thsxdxMultiplier)
    if (useDDN         == True) : clip = ddn(clip, bm3dSigma, ddnRemBinarize, smdThSAD)
    if (useUpscaling   == True) : clip = upscale(clip, isAnime, fsrcnnxPath, fsrcnnxLaPath, usWidth, usHeight)
    if (useEdgeHealing == True) : clip = edgeHealing(clip, useDehaloing, useDeringing, useAA, useUsAA)
    if (useDPIR        == True) : clip = dpir(clip, dpirTileDenominator, dpirDeblocking, dpirDenoising, dpirDeblockingStrength, dpirDenoisingStrength)
    if (useDebanding   == True) : clip = deband(clip, dbRemBinarize)
    if (useFinalizing  == True) : clip = finalize(clip)
    
    return clip