# facial_display.py

import pygame
import numpy as np
from typing import Optional

class FaceSprite:
    """Base class for facial features."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True
    
    def update(self, emotion: str, intensity: float):
        """Override in subclasses."""
        pass
    
    def draw(self, screen):
        """Override in subclasses."""
        pass


class Eyes(FaceSprite):
    """Eye sprites that change based on emotion."""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.eye_size = 20
        self.pupil_offset_x = 0
        self.pupil_offset_y = 0
        
    def update(self, emotion: str, intensity: float):
        """Adjust eyes based on emotion."""
        
        if emotion == 'happy':
            self.eye_size = 15  # Squinting (smiling eyes)
        elif emotion == 'surprised':
            self.eye_size = 30  # Wide open
        elif emotion == 'angry':
            self.pupil_offset_y = -5  # Looking down/intense
        else:
            self.eye_size = 20
            self.pupil_offset_y = 0
    
    def draw(self, screen):
        # Left eye
        pygame.draw.circle(screen, (255, 255, 255), 
                          (self.x - 40, self.y), self.eye_size)
        pygame.draw.circle(screen, (0, 0, 0), 
                          (self.x - 40, self.y), self.eye_size, 2)
        # Pupil
        pygame.draw.circle(screen, (0, 0, 0), 
                          (self.x - 40 + self.pupil_offset_x, 
                           self.y + self.pupil_offset_y), 
                          self.eye_size // 3)
        
        # Right eye (mirror)
        pygame.draw.circle(screen, (255, 255, 255), 
                          (self.x + 40, self.y), self.eye_size)
        pygame.draw.circle(screen, (0, 0, 0), 
                          (self.x + 40, self.y), self.eye_size, 2)
        pygame.draw.circle(screen, (0, 0, 0), 
                          (self.x + 40 + self.pupil_offset_x, 
                           self.y + self.pupil_offset_y), 
                          self.eye_size // 3)


class Mouth(FaceSprite):
    """Mouth that changes shape based on emotion."""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.curve_amount = 0  # Positive = smile, negative = frown
        self.width = 80
        
    def update(self, emotion: str, intensity: float):
        """Adjust mouth based on emotion and intensity."""
        
        if emotion == 'happy':
            self.curve_amount = int(20 + intensity * 30)  # Bigger smile
        elif emotion == 'sad':
            self.curve_amount = -int(20 + intensity * 30)  # Deeper frown
        elif emotion == 'angry':
            self.curve_amount = -int(10 + intensity * 20)
            self.width = int(60 + intensity * 30)  # Wider when angrier
        elif emotion == 'surprised':
            self.curve_amount = int(15)
            self.width = 40  # O shape
        else:
            self.curve_amount = 0
            self.width = 80
    
    def draw(self, screen):
        """Draw mouth as arc."""
        if self.curve_amount > 0:  # Smile
            start_angle = 0
            end_angle = np.pi
        else:  # Frown
            start_angle = np.pi
            end_angle = 2 * np.pi
        
        # Draw as arc
        rect = pygame.Rect(self.x - self.width//2, 
                          self.y - abs(self.curve_amount), 
                          self.width, 
                          abs(self.curve_amount) * 2)
        
        pygame.draw.arc(screen, (0, 0, 0), rect, 
                       start_angle, end_angle, 3)


class Eyebrows(FaceSprite):
    """Eyebrows for additional expression."""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.angle = 0  # Degrees of rotation
        self.height_offset = 0
        
    def update(self, emotion: str, intensity: float):
        """Adjust eyebrows."""
        
        if emotion == 'angry':
            self.angle = -15 * intensity  # Angled down
            self.height_offset = -int(5 * intensity)
        elif emotion == 'sad':
            self.angle = 15 * intensity  # Angled up (sad eyebrows)
            self.height_offset = int(5 * intensity)
        elif emotion == 'surprised':
            self.height_offset = int(10 * intensity)  # Raised
            self.angle = 0
        else:
            self.angle = 0
            self.height_offset = 0
    
    def draw(self, screen):
        """Draw eyebrows as lines."""
        # Left eyebrow
        start = (self.x - 60, self.y + self.height_offset)
        end = (self.x - 20, self.y + self.height_offset + int(self.angle))
        pygame.draw.line(screen, (0, 0, 0), start, end, 4)
        
        # Right eyebrow (mirror)
        start = (self.x + 20, self.y + self.height_offset + int(self.angle))
        end = (self.x + 60, self.y + self.height_offset)
        pygame.draw.line(screen, (0, 0, 0), start, end, 4)


class EmotionalFace:
    """Main face display using pygame."""
    
    def __init__(self, width=400, height=400):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CyberLife Face")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Face center
        center_x = width // 2
        center_y = height // 2
        
        # Create facial features
        self.face_circle = (center_x, center_y, 120)  # x, y, radius
        self.eyebrows = Eyebrows(center_x, center_y - 50)
        self.eyes = Eyes(center_x, center_y - 20)
        self.mouth = Mouth(center_x, center_y + 40)
        
        # Current emotion state
        self.current_emotion = 'neutral'
        self.facial_intensity = 0.5
    
    def update_from_matrix(self, emotion_matrix: np.ndarray, emotion_type: str):
        """
        Update face based on emotion regulation matrix.
        
        emotion_matrix: 4x4 numpy array
        emotion_type: 'happy', 'sad', 'angry', etc.
        """
        
        # Extract facial expression intensity from Row 2, Column 0
        self.facial_intensity = float(emotion_matrix[2, 0])
        self.current_emotion = emotion_type
        
        # Update all facial features
        self.eyebrows.update(emotion_type, self.facial_intensity)
        self.eyes.update(emotion_type, self.facial_intensity)
        self.mouth.update(emotion_type, self.facial_intensity)
    
    def update_from_memory(self, memory: dict):
        """Update face from stored memory."""
        
        emotion_key = list(memory['emotion'].keys())[0]
        regulation_data = memory['emotion'][emotion_key]['regulation']
        
        # Deserialize
        from numpy_utils.numpy_helpers import deserialize_numpy
        emotion_matrix = deserialize_numpy(regulation_data)
        
        # Update
        self.update_from_matrix(emotion_matrix, emotion_key)
    
    def draw(self):
        """Render the face."""
        
        # Clear screen
        self.screen.fill((240, 240, 240))
        
        # Draw face circle (head)
        pygame.draw.circle(self.screen, (255, 220, 177), 
                          (self.face_circle[0], self.face_circle[1]), 
                          self.face_circle[2])
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (self.face_circle[0], self.face_circle[1]), 
                          self.face_circle[2], 3)
        
        # Draw facial features
        self.eyebrows.draw(self.screen)
        self.eyes.draw(self.screen)
        self.mouth.draw(self.screen)
        
        # Display emotion info
        font = pygame.font.Font(None, 36)
        text = font.render(
            f"{self.current_emotion.upper()} | {self.facial_intensity:.2f}", 
            True, (0, 0, 0)
        )
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        """Main loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.draw()
            self.clock.tick(30)  # 30 FPS
        
        pygame.quit()
    
    def show_memory(self, memory: dict, duration_ms: int = 3000):
        """Display a memory's face for a duration."""
        
        self.update_from_memory(memory)
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration_ms:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
            
            self.draw()
            self.clock.tick(30)


# Usage
if __name__ == "__main__":
    # Test face
    face = EmotionalFace()
    
    # Simulate emotion changes
    test_matrix = np.array([
        [0.8, 0.5, 0.6, 0.3],  # Prefrontal
        [0.7, 0.6, 0.4, 0.8],  # Physiological
        [0.9, 0.7, 0.8, 0.9],  # Expression (Row 2, Col 0 = 0.9)
        [0.9, 0.5, 0.4, 0.9]   # Dopamine
    ])
    
    emotions = ['happy', 'sad', 'angry', 'surprised', 'neutral']
    
    for emotion in emotions:
        face.update_from_matrix(test_matrix, emotion)
        face.draw()
        pygame.time.wait(2000)  # 2 seconds each
    
    pygame.quit()