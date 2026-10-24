import cv2
import mediapipe as mp
import os
import math


# =========================================================
# MEDIAPIPE SETUP
# =========================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# =========================================================
# CAMERA SETUP
# =========================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not detected")
    exit()


# =========================================================
# IMAGE PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "images")

PIC1 = os.path.join(IMAGE_DIR, "pic1.png")
PIC2 = os.path.join(IMAGE_DIR, "pic2.png")
PIC3 = os.path.join(IMAGE_DIR, "pic3.png")
PIC4 = os.path.join(IMAGE_DIR, "pic4.png")
PIC5 = os.path.join(IMAGE_DIR, "pic5.png")


# =========================================================
# LOAD IMAGES
# =========================================================

images = {
    "PIC1": cv2.imread(PIC1),
    "PIC2": cv2.imread(PIC2),
    "PIC3": cv2.imread(PIC3),
    "PIC4": cv2.imread(PIC4),
    "PIC5": cv2.imread(PIC5)
}


# Check image loading

for name, img in images.items():

    if img is None:

        print(f"ERROR: {name} image not found")

    else:

        print(f"{name} loaded successfully")


# =========================================================
# FINGER DETECTION
# =========================================================

def fingers_up(lm, handedness="Right"):

    fingers = []

    # Thumb
    if handedness == "Right":

        thumb = lm[4].x < lm[3].x

    else:

        thumb = lm[4].x > lm[3].x

    fingers.append(thumb)


    # Index
    index = lm[8].y < lm[6].y

    fingers.append(index)


    # Middle
    middle = lm[12].y < lm[10].y

    fingers.append(middle)


    # Ring
    ring = lm[16].y < lm[14].y

    fingers.append(ring)


    # Pinky
    pinky = lm[20].y < lm[18].y

    fingers.append(pinky)


    return fingers


# =========================================================
# DISTANCE CALCULATION
# =========================================================

def calculate_distance(point1, point2):

    distance = math.sqrt(

        (point1.x - point2.x) ** 2 +

        (point1.y - point2.y) ** 2

    )

    return distance


# =========================================================
# PIC 4 - FINGER HEART GESTURE
# =========================================================

def finger_heart(hand_list):

    # Both hands must be detected

    if len(hand_list) != 2:

        return False


    detected_hearts = 0


    for hand in hand_list:

        lm = hand.landmark


        # Thumb tip
        thumb_tip = lm[4]


        # Index finger tip
        index_tip = lm[8]


        # Calculate distance
        distance = calculate_distance(

            thumb_tip,

            index_tip

        )


        # Hand size normalization
        hand_size = calculate_distance(

            lm[0],

            lm[9]

        )


        if hand_size == 0:

            return False


        normalized_distance = distance / hand_size


        # Finger-heart condition

        if normalized_distance < 0.65:

            detected_hearts += 1


    # Both hands must satisfy the condition

    return detected_hearts == 2


# =========================================================
# PIC 5 - BOTH HANDS OPEN
# =========================================================

def both_hands_open(hand_list, handedness_list):

    if len(hand_list) != 2:

        return False


    for i, hand in enumerate(hand_list):

        lm = hand.landmark


        if i < len(handedness_list):

            handedness = handedness_list[i]

        else:

            handedness = "Right"


        finger_states = fingers_up(

            lm,

            handedness

        )


        # All fingers extended

        if not all(finger_states):

            return False


    return True


# =========================================================
# DISPLAY IMAGE
# =========================================================

def display_image(image_name):

    img = images.get(image_name)


    if img is None:

        return


    resized_img = cv2.resize(

        img,

        (400, 400)

    )


    cv2.imshow(

        "Result",

        resized_img

    )


# =========================================================
# MAIN LOOP
# =========================================================

while True:


    # -----------------------------------------------------
    # READ CAMERA
    # -----------------------------------------------------

    ret, frame = cap.read()


    if not ret:

        print("Error reading camera")

        break


    # -----------------------------------------------------
    # FLIP CAMERA
    # -----------------------------------------------------

    frame = cv2.flip(

        frame,

        1

    )


    # -----------------------------------------------------
    # CONVERT TO RGB
    # -----------------------------------------------------

    rgb = cv2.cvtColor(

        frame,

        cv2.COLOR_BGR2RGB

    )


    # -----------------------------------------------------
    # PROCESS HANDS
    # -----------------------------------------------------

    results = hands.process(rgb)


    # -----------------------------------------------------
    # INITIALIZE
    # -----------------------------------------------------

    output = None

    hand_list = []

    handedness_list = []


    # -----------------------------------------------------
    # HAND DETECTION
    # -----------------------------------------------------

    if results.multi_hand_landmarks:


        hand_list = results.multi_hand_landmarks


        # -------------------------------------------------
        # HANDEDNESS
        # -------------------------------------------------

        if results.multi_handedness:

            for hand_info in results.multi_handedness:

                label = hand_info.classification[0].label

                handedness_list.append(label)


        # -------------------------------------------------
        # DRAW LANDMARKS
        # -------------------------------------------------

        for hand in hand_list:

            mp_draw.draw_landmarks(

                frame,

                hand,

                mp_hands.HAND_CONNECTIONS

            )


        # -------------------------------------------------
        # DISPLAY HAND COUNT
        # -------------------------------------------------

        hand_count = len(hand_list)


        cv2.putText(

            frame,

            f"Hands Detected: {hand_count}",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 0),

            2

        )


        # =================================================
        # PIC 4 - FINGER HEART
        # =================================================

        if finger_heart(hand_list):

            output = "PIC4"


        # =================================================
        # PIC 5 - BOTH HANDS OPEN
        # =================================================

        elif both_hands_open(

            hand_list,

            handedness_list

        ):

            output = "PIC5"


        # =================================================
        # EXISTING GESTURES
        # =================================================

        else:


            # Use first detected hand

            hand = hand_list[0]

            lm = hand.landmark


            # -------------------------------------------------
            # HANDEDNESS
            # -------------------------------------------------

            if handedness_list:

                handedness = handedness_list[0]

            else:

                handedness = "Right"


            # -------------------------------------------------
            # FINGER STATES
            # -------------------------------------------------

            thumb, index, middle, ring, pinky = fingers_up(

                lm,

                handedness

            )


            # -------------------------------------------------
            # INDEX FINGER POSITION
            # -------------------------------------------------

            ix = int(

                lm[8].x * frame.shape[1]

            )

            iy = int(

                lm[8].y * frame.shape[0]

            )


            # -------------------------------------------------
            # FRAME CENTER
            # -------------------------------------------------

            cx = frame.shape[1] // 2

            cy = frame.shape[0] // 2


            # -------------------------------------------------
            # PIC 1 - FINGER NEAR CENTER
            # -------------------------------------------------

            if (

                abs(ix - cx) < 70

                and

                abs(iy - cy) < 70

            ):

                output = "PIC1"


            # -------------------------------------------------
            # PIC 2 - THUMBS UP
            # -------------------------------------------------

            elif (

                thumb

                and

                not index

                and

                not middle

                and

                not ring

                and

                not pinky

            ):

                output = "PIC2"


            # -------------------------------------------------
            # PIC 3 - INDEX FINGER
            # -------------------------------------------------

            elif (

                index

                and

                not middle

                and

                not ring

                and

                not pinky

            ):

                output = "PIC3"


    # =====================================================
    # DISPLAY CAMERA
    # =====================================================

    cv2.imshow(

        "Camera",

        frame

    )


    # =====================================================
    # DISPLAY RESULT
    # =====================================================

    if output:

        display_image(output)


    # =====================================================
    # EXIT
    # =====================================================

    key = cv2.waitKey(1) & 0xFF


    if key == ord("q"):

        break


# =========================================================
# RELEASE CAMERA
# =========================================================

cap.release()


# =========================================================
# CLOSE WINDOWS
# =========================================================

cv2.destroyAllWindows()


# =========================================================
# CLOSE MEDIAPIPE
# =========================================================

hands.close()