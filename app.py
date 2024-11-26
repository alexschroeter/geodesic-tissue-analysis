from mikro_next.api.schema import Image,  from_array_like
from arkitekt_next import easy
from rekuest_next.agents.extensions.delegating.extension import CLIExtension
from rekuest_next.rekuest import RekuestNext
from arkitekt_next import register
from rekuest_next.register import register_structure
import tifffile
import os 
import xarray as xr
import rich_click as click
from rekuest_next.structures.parse_collectables import parse_collectable


@register_structure(identifier="OME_TIFF")
class OMETiffStructure:

    def __init__(self, file: str):
        self.file = file

    async def ashrink(self):
        return self.file
    
    @classmethod
    async def aexpand(cls, name: str):
        return cls(name)
    
    @classmethod
    def from_image(cls, image: Image):
        file_name = "image.tiff"
        tifffile.imwrite(file_name, image.data)
        return cls(file_name)
    
    def to_xarray(self) -> xr.DataArray:
        data = tifffile.imread(self.file)
        return data

    async def acollect(self):
        os.remove(self.file)
    


@register
def image_to_ome_tiff(image: Image) -> OMETiffStructure:
    return OMETiffStructure.from_image(image)


@register
def ome_tiff_to_timage(file: OMETiffStructure, name: str) -> Image:
    return from_array_like(file.to_xarray(), name=name)



@click.argument("script")
@click.command()
def run(script: str):
    
    app = easy()

    rekuest: RekuestNext = app.services.get("rekuest")

    rekuest.agent.register_extension("cli", CLIExtension(f"octave --no-gui --quiet {script}"))

    with app:
        try:
            app.run()
        except Exception:
            raise 



if __name__ == "__main__":
    run()