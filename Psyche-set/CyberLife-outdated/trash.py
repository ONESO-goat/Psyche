class Trash_or_Reuse:
    """Trash functions or Reuse later"""
    def __init__(self):
        self.name = "placeholder"
    def __create_model__(self):
        
        try:
            file = f"{self.name}_MODEL.py"
            with open(file, 'w') as f:
                f.write(self._model_())
        except IOError as e:
            raise IOError("There was an unexpected error when creating Brain Model: ", e)
        
    def _model_(self) -> str:
        script = f"""
from {self.name}_CONFIG import db
import uuid
from datetime import datetime
from sqlalchemy.dialects.sqlite import TEXT

{self.name.upper()}_ID = str(uuid.uuid4)

class {self.name}(db.Model):
    __tablename__ = "{self.name}BrainBase"

    Id = db.Column(TEXT, primary_key=True, default="{self.name}"+{self.name.upper()}_ID, unique=True, nullable=False)

    name = db.Column(db.String(120), nullable=False)

    WATTS = db.Column(db.Float, nullable=False)

    SIZE = db.Column(db.Float, nullable=False)

    CREATED_AT = db.Column(db.Date, nullable=False, default=datetime.utcnow())

    STORAGE = db.Column(TEXT, nullable=True)

"""
        return script  

    def setUP_storage(self, size: int):
        assert 0 < size <= 100, f"Inputed size ({size}) falls outside valid range (0 - 100)."
        storage = Storage(self.get_brain_data(), size)
        return storage  
    

    def showcase(self, 
                 figsize:tuple[int, int]=(7,7), 
                 border_color:str='black', 
                 color:str='gray', 
                 type:str='2D',
                 shape: str = 'circle', 
                 Brain_Size:float= 1.0) -> None:
        
        if type.upper() == '2D':
            fore, mid, hind = self.BrainCreation()
            plt.figure(figsize=figsize)
            plt.title("Brain Visualization")

            # Use circles to represent sections
            if shape.lower() == 'circle':
                circle_fore = Circle((Brain_Size, Brain_Size), fore, color=color, ec=border_color, alpha=0.6)
                #circle_mid = Circle((Brain_Size, Brain_Size), mid, color=color, ec=border_color, alpha=0.4)
                #circle_hind = Circle((Brain_Size, Brain_Size), hind, color=color, ec=border_color, alpha=0.2)
            elif shape.lower() == 'rectangle' or shape.lower() == 'rec':
                ...
            else:
                raise ValueError(f"""Invalid shape: ({shape.lower()}). Please choose either 
                                 (circle => default) or (rectangle).""")
            fig, ax = plt.subplots()
            #ax.add_artist(circle_hind)
           # ax.add_artist(circle_mid)
            ax.add_artist(circle_fore)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            plt.show()
        elif type.upper() == '3D':
            # TODO
            """
            Implement a system where it showcases a 3D circle (for now)
            """
            ...
        else:
            raise ValueError(f"The type ({type}) is not valid. Valid types include 2D or 3D Visualization.")







    def _create_config_(self, auto_Activation: bool = False):

        import uuid
        import importlib as lib
        from pathlib import Path
        import os
        import sys
        
        try:
            
            id = str(uuid.uuid4())
            file = f"{self.name}_CONFIG.py" 
            path = Path(id) / Path(file)
            with open(file, 'w') as f:
                f.write(self._())
            if auto_Activation:
                lib.invalidate_caches()

                if os.getcwd() not in sys.path:
                    sys.path.append(os.getcwd())

                module = lib.import_module(file[:-3].strip())
                module.run()
                
        except IOError as e:
            raise IOError("There was an error creating brain database: ", e)
    