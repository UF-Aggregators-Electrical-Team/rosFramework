import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import CameraInfo

class intelRealSenseSubscriberNode(Node):
    def __init__(self) -> None:
        super().__init__("camera_info_subber")
        self.intel_subber = self.create_subscription(
            CameraInfo, 
            "/camera/color/camera_info",
            self.intel_callback,
            10
        )
    def intel_callback(self, msg: CameraInfo):
        self.get_logger().info(str(msg))
        # print(str(msg))


def main(args=None):
    rclpy.init(args=args)
    node = intelRealSenseSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()
