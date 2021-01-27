# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Read-with-rasterio" data-toc-modified-id="Read-with-rasterio-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Read with rasterio</a></span></li><li><span><a href="#Find-an-interesting-subset" data-toc-modified-id="Find-an-interesting-subset-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Find an interesting subset</a></span></li><li><span><a href="#Define-inputs-and-pixel_adjust-func" data-toc-modified-id="Define-inputs-and-pixel_adjust-func-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Define inputs and <code>pixel_adjust</code> func</a></span></li><li><span><a href="#Explore" data-toc-modified-id="Explore-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Explore</a></span></li><li><span><a href="#Output" data-toc-modified-id="Output-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Output</a></span></li></ul></div>

import rasterio
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import panel as pn
pn.extension()

# ### Read with rasterio
# `'example.tiff'` is band 1 from Landsat `LC08_L1TP_037034_20200925_20201006_01_T1`, linked [here](https://landsatonaws.com/L8/037/034/LC08_L1TP_037034_20200925_20201006_01_T1)

dataset = rasterio.open('example.tiff')
band1 = dataset.read(1)

# ### Find an interesting subset

# +
fig,ax = plt.subplots(1, 2)

x = 3500 # anchor on x-axis
y = 5000 # anchor on y-axis
extent = 1000 # linear extent

ax[0].imshow(band1)
rect = patches.Rectangle((x, y), extent, extent,
                         linewidth=1,edgecolor='r',facecolor='none')
ax[0].add_patch(rect)

inset = band1[x:x+extent, y:y+extent]
ax[1].imshow(inset)
# -

# ### Define inputs and `pixel_adjust` func

x_slider = pn.widgets.IntSlider(name='x', start=0, end=extent, step=50, value=300)
y_slider = pn.widgets.IntSlider(name='y', start=0, end=extent, step=50, value=400)
extent_slider = pn.widgets.IntSlider(name='extent', start=1, end=extent, step=50, value=400)
delta_slider = pn.widgets.IntSlider(name='delta', start=-5000, end=5000, step=100, value=0)


@pn.depends(x_slider.param.value, y_slider.param.value, 
            extent_slider.param.value, delta_slider.param.value)
def pixel_adjust(x=x_slider.param.value,
                 y=y_slider.param.value,
                 ext=extent_slider.param.value, 
                 d=delta_slider.param.value, 
                 raster=inset):
    '''
    x is the x index
    y is the y index
    ext is the extents of the bounding box. 1 means a single pixel
    d is the delta
    rast is the input raster
    '''
    fig,ax = plt.subplots(1)
    im = raster.copy()
    
    # highlight the selection pixel and/or area
    ax.vlines(x=x, ymin=0, ymax=im.shape[1])
    ax.hlines(y=y, xmin=0, xmax=im.shape[0])
    rect = patches.Rectangle((x, y), ext, ext,
                             linewidth=1,edgecolor='r',facecolor='none')
    
    # apply the delta to the selected pixel and/or area
    im[y:y+ext, x:x+ext] = im[y:y+ext, x:x+ext] + d
    
    ax.imshow(im)
    ax.add_patch(rect)
    plt.close()
    return fig


# ### Explore

pn.Row(
    pixel_adjust,
    pn.Column(
        x_slider,
        y_slider,
        extent_slider,
        delta_slider
    )
).servable()


