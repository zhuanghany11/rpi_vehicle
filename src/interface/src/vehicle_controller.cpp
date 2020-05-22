#include <iostream>
#include "ros/ros.h"
#include "common/RemoteControlMsg.h"
#include <wiringPi.h>
#include <softPwm.h>

#define ENA 13	// L298P enable A. Right Motor
#define ENB 20  // L298P enable B. Left Motor
#define IN1 16  // L298P input 1. Right Motor +
#define IN2 19  // L298P input 2. Right Motor -
#define IN3 26  // L298P input 3. Left Motor +
#define IN4 21  // L298P input 4. Left Motor -

class VehicleController
{
private:
    ::ros::NodeHandle m_rosnode;
    ::ros::Subscriber m_control_subscriber {m_rosnode.subscribe("remote_control", 10, &VehicleController::callbackRemoteControl, this)};
	::ros::Rate m_rate {20};

	bool m_shutdown = false;
	bool m_initialized = false;
	int32_t m_rightwheel = 0;
	int32_t m_leftwheel = 0;

public:
	VehicleController() {}

	~VehicleController() {}

	void initialize()
	{
  		int ret = wiringPiSetupGpio();
		if (ret == -1) 
		{
			ROS_ERROR("[Control]GPIO Initialized Failed!");
			return;
		}
		else
		{
			ROS_INFO("[Control]GPIO Initialized!");
			pinMode(IN1, OUTPUT);
			pinMode(IN2, OUTPUT);
			pinMode(IN3, OUTPUT);
			pinMode(IN4, OUTPUT);

			pinMode(ENA, SOFT_PWM_OUTPUT) ;
			int retA = softPwmCreate(ENA, 0, 100);
			pinMode(ENB, SOFT_PWM_OUTPUT) ;
			int retB = softPwmCreate(ENB, 0, 100);
			
			if(retA == 0 || retB == 0)
			{
				ROS_ERROR("[Control]PWM Pins Initialized Failed!");
			}
			else
			{
				ROS_INFO("[Control]PWM Pins Initialized!");
				m_initialized = true;
			}
		}
	}

	void run()
	{
		if(!m_initialized) return;
		
		while(ros::ok() && !m_shutdown)
		{
			int32_t rightPWM = 0;
			int32_t leftPWM = 0;
			char rightDir = '0';
			char leftDir = '0';
			
			if(m_rightwheel >= 0)
			{
				digitalWrite(IN1, HIGH);
				digitalWrite(IN2, LOW);
				rightDir = '+';
				if (m_rightwheel <= 100) rightPWM = m_rightwheel;
				else rightPWM = 100;
			}
			else
			{
				digitalWrite(IN1, LOW);
				digitalWrite(IN2, HIGH);
				rightDir = '-';
				if (m_rightwheel >= -100) rightPWM = -m_rightwheel;
				else rightPWM = 100;
			}

			if(m_leftwheel >= 0)
			{
				digitalWrite(IN3, HIGH);
				digitalWrite(IN4, LOW);
				leftDir = '+';
				if (m_leftwheel <= 100) leftPWM = m_leftwheel;
				else leftPWM = 100;
			}
			else
			{
				digitalWrite(IN3, LOW);
				digitalWrite(IN4, HIGH);
				leftDir = '-';
				if (m_leftwheel >= -100) leftPWM = -m_leftwheel;
				else leftPWM = 100;
			}

			softPwmWrite(ENA, rightPWM);
			softPwmWrite(ENB, leftPWM);

			ROS_INFO("[Control]GPIO Output: %c%d | %c%d", leftDir, leftPWM, rightDir, rightPWM);

			::ros::spinOnce();
			m_rate.sleep();
		}
	}

	void shutdown()
	{
		m_shutdown = true;
	}

private:
	void callbackRemoteControl(const common::RemoteControlMsgConstPtr& msg)
	{
		ROS_INFO("[Control][RxMsg]Status: %d. Wheels: %d | %d.", msg->status, msg->leftwheel, msg->rightwheel);
		m_rightwheel = msg->rightwheel;
		m_leftwheel = msg->leftwheel;
	}
};
 
int main(int argc, char **argv)
{
	::ros::init(argc, argv, "vehicle_controller");

    VehicleController vehicle_controller;
	vehicle_controller.initialize();
	vehicle_controller.run();
	
	return 0;
}

