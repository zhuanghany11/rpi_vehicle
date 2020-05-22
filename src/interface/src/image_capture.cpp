#include <opencv2/opencv.hpp>
#include "ros/ros.h"
#include "sensor_msgs/CompressedImage.h"
#include "sensor_msgs/Image.h"
#include "sensor_msgs/fill_image.h"
#include <vector>

class ImageCapture
{
private:
	::cv::VideoCapture m_camera;
	::cv::Mat m_image;
    ::ros::NodeHandle m_rosnode;
    ::ros::Publisher m_compressed_image_publisher {m_rosnode.advertise<sensor_msgs::CompressedImage>("front_camera/compressed", 1, true)}; 
	//::ros::Publisher m_image_publisher {m_rosnode.advertise<sensor_msgs::Image>("front_camera", 1, true)}; 
	::ros::Rate m_rate{10};

	bool m_shutdown = false;
	bool m_initialized = false;
	uint32_t m_header_seq = 0;

public:
	ImageCapture() {}

	~ImageCapture() {}

	void initialize()
	{
  		m_camera.open(0);
		if(!m_camera.isOpened()) 
		{
			ROS_ERROR("[Camera]Camera opening failed!");
			return;
		}
		else
		{
			m_camera.set(CV_CAP_PROP_FRAME_WIDTH, 352U);
			m_camera.set(CV_CAP_PROP_FRAME_HEIGHT, 288U);
			m_camera.set(CV_CAP_PROP_FOURCC, CV_FOURCC('M', 'J', 'P', 'G'));
			m_camera.set(CV_CAP_PROP_BUFFERSIZE, 1); 
			ROS_INFO("[Camera]Camera opening succeeded!");
			m_initialized = true;
		}
	}

	void run()
	{
		if(!m_initialized) return;
		
		while(ros::ok() && !m_shutdown)
		{
			//::cv::Mat m_capture;
			//m_camera >> m_capture;
			//::cv::resize(m_capture, m_image, ::cv::Size(400U, 300U));
			m_camera >> m_image;
			::std::vector<uchar> data_encoded;
			::cv::imencode(".jpeg", m_image, data_encoded);
			
			//ROS_INFO("height: %d, width: %d.\n", m_image.rows, m_image.cols);
			//::sensor_msgs::Image raw_img;
			//::sensor_msgs::fillImage(raw_img, "rgb8", 300U, 400U, 400U * 3U , m_image.data);
			//raw_img.header.stamp = ::ros::Time::now();
			//raw_img.header.seq = m_header_seq;
			//m_image_publisher.publish(raw_img);

			::sensor_msgs::CompressedImage jpeg_img;
			jpeg_img.data.swap(data_encoded);
			jpeg_img.format = "jpeg";
			jpeg_img.header.stamp = ::ros::Time::now();
			jpeg_img.header.seq = m_header_seq;
			m_compressed_image_publisher.publish(jpeg_img);
			//::cv::imshow("Front Camera", m_image);
			//::cv::waitKey(1);
			++ m_header_seq;
			m_rate.sleep();
		}
	}

	void shutdown()
	{
		m_shutdown = true;
	}

private:

};
 
int main(int argc, char **argv)
{
	::ros::init(argc, argv, "image_capture");

    ImageCapture image_capture;
	image_capture.initialize();
	image_capture.run();
	
	return 0;
}

