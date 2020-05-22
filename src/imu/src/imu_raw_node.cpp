#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include "ros/ros.h"
#include "sensor_msgs/Imu.h"
#include <sstream>
#include "sensor_msgs/MagneticField.h"


// class IMU()
// {
// private:
//   int m_MPU9250;
//   int m_AK8963; 
//   int16_t m_data_raw[9] = {0};
//   float m_data_converted[9] = {0.0f};
//   bool m_initialized = false;
//   float m_acc_conversion = 

// public:
//   IMU(){
//   }

//   ~IMU(){}
  
//   int initialize(){
//     wiringPiSetupSys();
//     m_MPU9250 = wiringPiI2CSetup(0x68);
//     if (m_MPU9250 == -1) {
//       printf("no accel-gyro(MPU6500) i2c device found\n");
//       m_initialized = false;
//       return -1;
//     }

//     wiringPiI2CWriteReg8(m_MPU9250, 0x6b, 0x80); // Reset pull up
//     sleep(0.1);
//     wiringPiI2CWriteReg8(m_MPU9250, 0x6b, 0x00); // Reset finish

//     // To read the magnetometer, the MPU9250 need to be set into bypass mode to let raspi to readl the magnetometer data.
//     // First, write INT_PIN_CFG(0x37) with a data 0x02. This data 0x02 means 00000010 to enable bypass.
//     //
//     // Finally, read the i2c device with address 0x0c.
//     //  
//     // Add  Name        Serial  Bit7  Bit6    Bit5          Bit4              Bit3          Bit2              Bit1      Bit0
//     // 0x37 INT_PIN_CFG R/W     ACTL  OPEN    LATCH_INT_EN  INT_ANYRD_2CLEAR  ACTL_FSYNC    FSYNC_INT_MODE_EN BYPASS_EN -
//     wiringPiI2CWriteReg8(m_MPU9250, 0x37, 0x02);
//     m_AK8963 = wiringPiI2CSetup(0x0c);
//     if (m_AK8963 == -1) {
//       printf("no mag(AK8963) i2c device found\n");
//       m_initialized = false;
//       return -1;
//     }
//     m_initialized = true;
//   }
  
//   void readData()
//   {
//     //acclerometer
//     m_data_raw[0] = (wiringPiI2CReadReg8 (m_MPU9250, 0x3B)<<8)|wiringPiI2CReadReg8 (m_MPU9250, 0x3C);
//     m_data_raw[1] = (wiringPiI2CReadReg8 (m_MPU9250, 0x3D)<<8)|wiringPiI2CReadReg8 (m_MPU9250, 0x3E);
//     m_data_raw[2] = (wiringPiI2CReadReg8 (m_MPU9250, 0x3F)<<8)|wiringPiI2CReadReg8 (m_MPU9250, 0x40);
//     m_data_converted[0] = m_data_raw[0] * m_acc_conversion;
//     m_data_converted[1] = m_data_raw[1] * m_acc_conversion;
//     m_data_converted[2] = m_data_raw[2] * m_acc_conversion;

//     //gyroscope
//     m_data_raw[3] = (wiringPiI2CReadReg8 (m_MPU9250, 0x43)<<8)|wiringPiI2CReadReg8 (m_MPU9250, 0x44) 
//     m_data_raw[4] = (wiringPiI2CReadReg8 (m_MPU9250, 0x45)<<8)|wiringPiI2CReadReg8 (m_MPU9250, 0x46);
//     m_data_raw[5] = (wiringPiI2CReadReg8 (m_MPU9250, 0x47)<<8)|wiringPiI2CReadReg8 (m_MPU9250, 0x48); 
//     m_data_converted[0] = m_data_raw[0] * m_acc_conversion;
//     m_data_converted[1] = m_data_raw[1] * m_acc_conversion;
//     m_data_converted[2] = m_data_raw[2] * m_acc_conversion;


//     //magnentometer
//     // Need to set to single read, then wait the data ready, then read the data.
//     uint8_t ST1;
//     wiringPiI2CWriteReg8(dev_mag, 0x0A, 0x01); 
//     do
//     {
//       ST1 = wiringPiI2CReadReg8(dev_mag, 0x02);
//     } while (!(ST1 & 0x01));

//     InBuffer[6]=  (wiringPiI2CReadReg8 (dev_mag, 0x04)<<8)|wiringPiI2CReadReg8 (dev_mag, 0x03);
//     InBuffer[7]=  (wiringPiI2CReadReg8 (dev_mag, 0x06)<<8)|wiringPiI2CReadReg8 (dev_mag, 0x05);
//     InBuffer[8]=  (wiringPiI2CReadReg8 (dev_mag, 0x08)<<8)|wiringPiI2CReadReg8 (dev_mag, 0x07);

//   }

// };

int main(int argc, char **argv){

  ros::init(argc, argv, "imu_raw_node");
  
  ros::NodeHandle n;
  ros::Publisher pub_imu = n.advertise<sensor_msgs::Imu>("imu/data_raw", 2);
  ros::Publisher pub_mag = n.advertise<sensor_msgs::MagneticField>("imu/mag", 2);

	int dev_acc_gyro;
  int dev_mag; 
  wiringPiSetupSys();

  dev_acc_gyro = wiringPiI2CSetup(0x68);
	if (dev_acc_gyro == -1) {
    printf("no accel-gyro(MPU6500) i2c device found\n");
    return -1;
	}
  wiringPiI2CWriteReg8(dev_acc_gyro, 0x6b, 0x80); // Reset pull up
  sleep(0.1);
  wiringPiI2CWriteReg8(dev_acc_gyro, 0x6b, 0x00); // Reset finish

  // To read the magnetometer, the MPU9250 need to be set into bypass mode to let raspi to readl the magnetometer data.
  // First, write INT_PIN_CFG(0x37) with a data 0x02. This data 0x02 means 00000010 to enable bypass.
  //
  // Finally, read the i2c device with address 0x0c.
  //  
  // Add  Name        Serial  Bit7  Bit6    Bit5          Bit4              Bit3          Bit2              Bit1      Bit0
  // 0x37 INT_PIN_CFG R/W     ACTL  OPEN    LATCH_INT_EN  INT_ANYRD_2CLEAR  ACTL_FSYNC    FSYNC_INT_MODE_EN BYPASS_EN -
  wiringPiI2CWriteReg8(dev_acc_gyro, 0x37, 0x02);
  dev_mag = wiringPiI2CSetup(0x0c);
	if (dev_mag == -1) {
    printf("no mag(AK8963) i2c device found\n");
    return -1;
	}

  int16_t InBuffer[9] = {0}; 

  ::ros::Rate rate = 50;

  while (ros::ok()){
    //http://docs.ros.org/api/sensor_msgs/html/msg/Imu.html 
    //http://docs.ros.org/api/sensor_msgs/html/msg/MagneticField.html
    sensor_msgs::Imu data_imu;    
    sensor_msgs::MagneticField data_mag;

    float conversion_gyro = 3.1415/(180.0*131.0f);
    float conversion_acce = 9.8/16384.0f;
    InBuffer[0] = (wiringPiI2CReadReg8 (dev_acc_gyro, 0x3B)<<8)|wiringPiI2CReadReg8 (dev_acc_gyro, 0x3C);
    InBuffer[1] = (wiringPiI2CReadReg8 (dev_acc_gyro, 0x3D)<<8)|wiringPiI2CReadReg8 (dev_acc_gyro, 0x3E);
    InBuffer[2] = (wiringPiI2CReadReg8 (dev_acc_gyro, 0x3F)<<8)|wiringPiI2CReadReg8 (dev_acc_gyro, 0x40);

    //gyroscope
    InBuffer[3] = (wiringPiI2CReadReg8 (dev_acc_gyro, 0x43)<<8)|wiringPiI2CReadReg8 (dev_acc_gyro, 0x44);
    InBuffer[4] = (wiringPiI2CReadReg8 (dev_acc_gyro, 0x45)<<8)|wiringPiI2CReadReg8 (dev_acc_gyro, 0x46);
    InBuffer[5] = (wiringPiI2CReadReg8 (dev_acc_gyro, 0x47)<<8)|wiringPiI2CReadReg8 (dev_acc_gyro, 0x48); 

    //magnentometer
    // Need to set to single read, then wait the data ready, then read the data.
    uint8_t ST1;
    wiringPiI2CWriteReg8(dev_mag, 0x0A, 0x01); 
    do
    {
      ST1 = wiringPiI2CReadReg8(dev_mag, 0x02);
    } while (!(ST1 & 0x01));

    InBuffer[6] = (wiringPiI2CReadReg8 (dev_mag, 0x04)<<8)|wiringPiI2CReadReg8 (dev_mag, 0x03);
    InBuffer[7] = (wiringPiI2CReadReg8 (dev_mag, 0x06)<<8)|wiringPiI2CReadReg8 (dev_mag, 0x05);
    InBuffer[8] = (wiringPiI2CReadReg8 (dev_mag, 0x08)<<8)|wiringPiI2CReadReg8 (dev_mag, 0x07);

    data_imu.linear_acceleration.x = -InBuffer[0]*conversion_acce;
    data_imu.linear_acceleration.y = -InBuffer[1]*conversion_acce;
    data_imu.linear_acceleration.z = InBuffer[2]*conversion_acce;
    
    data_imu.angular_velocity.x = -InBuffer[3]*conversion_gyro;
    data_imu.angular_velocity.y = -InBuffer[4]*conversion_gyro;
    data_imu.angular_velocity.z = InBuffer[5]*conversion_gyro; 

    data_mag.magnetic_field.x = InBuffer[6]*0.6f;
    data_mag.magnetic_field.y = InBuffer[7]*0.6f;
    data_mag.magnetic_field.z = InBuffer[8]*0.6f;

    data_mag.header.stamp = ros::Time::now();
    data_imu.header.stamp = data_mag.header.stamp;
    data_imu.header.frame_id = "/imu_link";

    pub_imu.publish(data_imu);
    pub_mag.publish(data_mag);
    rate.sleep();
    }
  return 0;
 }
