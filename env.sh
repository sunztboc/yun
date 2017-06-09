sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
setenforce 0
systemctl stop firewalld
systemctl disable firewalld
sed -i "s:mirrorlist=http\://mirrorlist.centos.org:#mirrorlist=http\://mirrorlist.centos.org:g" /etc/yum.repos.d/CentOS-Base.repo
sed -i "s:#baseurl=http\://mirror.centos.org:baseurl=http\://mirrors.aliyun.com:g" /etc/yum.repos.d/CentOS-Base.repo
yum install lrzsz chrony gcc gcc-c++ git openssl-devel perl-ExtUtils-CBuilder perl-ExtUtils-MakeMaker wget screen -y
systemctl enable chronyd
systemctl start chronyd
