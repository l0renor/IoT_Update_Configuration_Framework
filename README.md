# IoT_Update_Configuration_Framework
A framework written for my bachlor thesis to securly update and configure IoT devices.

## Thesis: architecture and implementation of a secure iot management solution
### Abstract
Despite the strong growth of the IoT industry, IoT management systems are usually
developed without the necessary security measures. This creates profound dangers for
companies, private individuals, as well as society in general.
In this thesis the dangers for an IoT management solution are analyzed and techniques
for safeguarding such systems are elucidated. Especially the security of the update
process as well as the security of the online management systems will be addressed.
Subsequently, the architecture of a secure management solution is proposed with the
help of the frameworks The Update Framework (TUF) and Django. The architecture
comprises a server that allows users to install and configure applications on the IoT
device via a web interface. Furthermore, it distributes software updates and configuration
data to the clients. The client-side implementation downloads configurations and updates
from the server and manages the installed applications as child processes. The proposed
architecture is created in a Python implementation and deployed on a Raspberry Pi
single-board computer. Finally, the developed solution is evaluated regarding its usability
and security.
Overall, it was established that such an application can be developed securely using
standardised security measures and prioritising safety throughout the entire development
process, without being required to program cryptographic procedures oneself. This way
a costly and fault-prone work step can be avoided.
