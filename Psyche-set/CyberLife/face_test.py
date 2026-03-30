from BrainAnomaly.BrainAnomaly import Brain
from Memory.Emotions.Headquarters import Headquarters
import numpy as np
from Memory.Emotions.Face_Display.Face_display_claude import EmotionalFace


def face_test():
    
    

    # Create brain and load memory
    brain = Brain(name="Test")
    hq = Headquarters(brain.mind.get_all(), brain)

    # Focus on a memory
    hq.focus(brain.mind.find(id='367de4b5-7d4d-45d8-9a82-e5e03bc9ab4e'))
    print(brain.mind.find(id='367de4b5-7d4d-45d8-9a82-e5e03bc9ab4e'))

    # Create face display
    face = EmotionalFace()
    print(f"""
\n\n
        ROW1 {hq.ROW1.first_row}
        ROW2 {hq.ROW2.second_row}
        ROW3 {hq.ROW3.third_row}
        ROW4 {hq.ROW4.fourth_row}


""")
    # Show the focused memory's face
    emotion_matrix = np.array([
        hq.ROW1.first_row,
        hq.ROW2.second_row,
        hq.ROW3.third_row,
        hq.ROW4.fourth_row
    ])

    face.update_from_matrix(emotion_matrix, emotion_type=hq.focused_memory_operator)
    face.run()

if __name__ == "__main__":
    face_test()