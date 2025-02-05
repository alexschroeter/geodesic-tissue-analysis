from mikro_next.api.schema import Image, File, Table, from_array_like
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
import pymeshlab
import pandas as pd

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


@register_structure(identifier="MESH")
class MeshStructure:

    def __init__(self, file: str):
        self.file = file
        self.ms = pymeshlab.MeshSet()

    async def ashrink(self):
        return self.file

    @classmethod
    async def aexpand(cls, name: str):
        return cls(name)
    
    @classmethod
    def from_file(cls, mesh_data):
        file_name = "mesh.obj"
        cls.ms.save_current_mesh(file_name)
        return cls(file_name)

    def to_meshlabdata(self):
        with open(self.file, 'r') as f:
            self.ms.load_new_mesh(f)
            return self.ms

    async def acollect(self):
        os.remove(self.file)


@register_structure(identifier="CSV")
class CSVStructure:

    def __init__(self, file: str):
        self.file = file

    async def ashrink(self):
        return self.file

    @classmethod
    async def aexpand(cls, name: str):
        return cls(name)

    @classmethod
    def from_table(cls, csv_data: Table):
        file_name = "data.csv"
        df = pd.to_csv(file_name)
        return cls(file_name)

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(self.file)
        return df

    async def acollect(self):
        os.remove(self.file)


@register
def image_to_ome_tiff(image: Image) -> OMETiffStructure:
    return OMETiffStructure.from_image(image)


@register
def ome_tiff_to_timage(file: OMETiffStructure, name: str) -> Image:
    return from_array_like(file.to_xarray(), name=name)


@register
def mesh_to_structure(mesh_data: File) -> MeshStructure:
    return MeshStructure.from_mesh(mesh_data)


@register
def structure_to_mesh(file: MeshStructure):
    return file.to_mesh()


@register
def csv_to_structure(csv_data: Table) -> CSVStructure:
    return CSVStructure.from_csv(csv_data)


@register
def structure_to_csv(file: CSVStructure):
    return file.to_csv()


@click.argument("script")
@click.command()
def run(script: str):
    
    app = easy("fuck_matlab_twice", url="arkitekt.compeng.uni-frankfurt.de")

    rekuest: RekuestNext = app.services.get("rekuest")

    async def on_init(handle):
        print("running on init")
        print(await handle.read(until="Enter: "))
        await handle.write("aleschro@em.uni-frankfurt.de")
        print(await handle.read("Enter: "))
        await handle.write(f"******")


    async def on_print(x):
        print(x)


    rekuest.agent.register_extension("cli", CLIExtension(run_script=f'''/bin/run.sh -nodesktop -nosplash -nodisplay -r "run('/home/matlab/{script}'); exit;"''', on_process_stdout=on_print, initial_timeout=60))

    with app:
        try:
            app.run()
        except Exception:
            raise 


if __name__ == "__main__":
    run()
