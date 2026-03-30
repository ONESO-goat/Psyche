from typing import Dict, List, Any

class _Structure:
    def __init__(self):
        ...
    def _create_structure(self, name) -> Dict[str, Any]:
        """It's reconmmended that you the user dont use this class and tocuh
        any of it's functions as it can cause random and unexplained bugs
        which can cause unwanted behavior."""
        import uuid
        from datetime import datetime, date
        import numpy as np
        structure = {
            'brain': {
                'id': str(uuid.uuid4()),

                '_personal_data': {
                    'name': {'name': name, 'nickname': []},
                    'firends': {}
                },

                'mind':[],
                
                'current_objective': [],

                'main_objectives': [],

                'current_objectives': [],

                'main_goal': [],

                'overall_Enthusiam': {
                    'inspiration': {
                        'scale': 0.0,
                        'details': 'No data avilable for this brain yet.'
                    },
                    'motivation': {
                        'scale': 0.0,
                        'details': 'No data avilable for this brain yet.'
                    }
                    
                },

                '_existence': {
                    '_date': date.today().isoformat(),
                    '_exact_date': datetime.utcnow().isoformat(),
                    
                },

                'decayed_memories': []

            }
        }
        return structure
if __name__ == "__main__":
    pass