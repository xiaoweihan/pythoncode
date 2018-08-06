//C++定义的名空间
namespace cpp Connector

//python定义的名空间
namespace py Connector

struct ConvertElement
{
   1:string strResultDir;
   2:string strCopyDir;
   3:string strHtcFilePath;
   4:double costTime;

}

//服务名称
service ResultConverter
{
  //把HAWC2生成的sel文件以及dat文件解析转换成hdf5文件
  bool ConvertResult(1:ConvertElement element)
}