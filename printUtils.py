import cv2


def print_and_view_detections(detected_objects, screen_width=1280, screen_height=720):
    print(f"Total objects stored: {len(detected_objects)}")
    for obj_id, obj in detected_objects.items():
        print(f"ID: {obj_id}, Label: {obj.label}, Score: {obj.score:.4f}")

        window_name = f"Object {obj_id} - {obj.label}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, screen_width, screen_height)
        cv2.imshow(window_name, obj.masked_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

def show_frames_in_loop(result, screen_width=1280, screen_height=720):
    frame_ = result.plot()
    window_name = 'Boxes and Masks Video'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, screen_width, screen_height)
    cv2.imshow(window_name, frame_)
    cv2.waitKey(1) 
