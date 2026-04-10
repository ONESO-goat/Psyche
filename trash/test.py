

def test1():

    try:
        from picamera import PiCamera
        from time import sleep
        
        camera = PiCamera()
        camera.start_preview()
        sleep(5)
        camera.stop_preview()
        return {'works': True, 'package': 'picamera'}
    
    except Exception as ex:
        print(f"[test 1] PICAMERA Error: {ex}")
        return {'works': False, 'package': 'picamera'}


def test2():

    try:
        from picamera2 import Picamera2
        from time import sleep
        
        camera = Picamera2()
        camera.configure(camera.create_preview_configuration())
        camera.start()
        sleep(5)
        camera.stop()
        
        return {'works': True, 'package': 'picamera2'}
    
    except Exception as ex:
        print(f"[test 2] PICAMERA2 Error: {ex}")
        return {'works': False, 'package': 'picamera2'}

def test3(index:int=0):
    try:
        import cv2
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            raise Exception("Camera failed to open")

        ret, frame = cap.read()
        if not ret:
            raise Exception("Failed to read frame")

        cap.release()
        return {'works': True, 'package': 'opencv'}
    
    except Exception as ex:
        print(f"[test 3] OpenCV Error: {ex}")
        return {'works': False, 'package': 'opencv'}
    
if __name__ == "__main__":

    test = {
        '1': test1,
        '2': test2,
        '3': test3
    }
    
    runs = [i() for i in test.values()]
    what_works = []
    
    for package in runs:
        if package['works']:
            what_works.append(package['package'])
        else:
            continue
    
    if not what_works:
        print("""\n
              None of the packages work on your end.
              
              first read the exceptions
              
              Then run these:
              
              lsusb -> should return a list of usb connected devices
              
              v4l2-ctl --list-devices -> just the same as lsusb
              
              libcamera-hello -> might open a camera on your end\n
              """)
    else:
        print("SOMETHING WORKS! :)")
        print(f"WHAT WORKS: {what_works}")
            
            
    
    
    
    