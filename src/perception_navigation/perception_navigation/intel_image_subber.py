import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class intelRealSenseSubscriberNode(Node):
    def __init__(self) -> None:
        super().__init__("camera_image_subber")
        self.bridge = CvBridge()
        self.intel_subber = self.create_subscription(
            Image, 
            "/camera/color/image_raw",
            self.intel_callback,
            10
        )
        self.intel_pubber = self.create_publisher(Image, '/out/image', 3)
    def intel_callback(self, inp_im):
        try: 
            imCV = self.bridge.imgmsg_to_cv2(inp_im, "bgr8")
        except CvBridgeError as e:
            print(e)

        if imCV is None:
            print('frame dropped, skipping tracking')
        else:
            self.ImageProcessor(imCV)

    def ImageProcessor(self, imCV):
        faceCascade = cv2.CascadeClassifier('/home/aggregator/ros2_ws/src/perception_navigation/perception_navigation/haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(imCV, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags = cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            cv2.rectangle(imCV, (x,y), (x+w, y+h), (0,255,0), 2)

        imCV = self.bridge.cv2_to_imgmsg(imCV, "bgr8")

        self.intel_pubber.publish(imCV)

def main(args=None):
    rclpy.init(args=args)
    node = intelRealSenseSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()
