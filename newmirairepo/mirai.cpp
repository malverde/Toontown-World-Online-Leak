// mirai.cpp : Defines the entry point for the console application.
//

#include <Python.h>
#include <marshal.h>
#include <iostream>
#include <string>
#include <cstdlib>
#include <fstream>
#include <openssl/evp.h>
#include <vector>

class Reader
{
	char* m_buf;
	unsigned int m_buflen;
	unsigned int m_pos;
	public:
		Reader(char* buf, unsigned int buflen) : m_buf(buf),
			m_buflen(buflen), m_pos(0)
		{
		}

		char* ReadCString()
		{
			std::string out;
			while(m_pos < m_buflen && m_buf[m_pos])
			{
				out += m_buf[m_pos];
				m_pos++;
			}
			m_pos++;
			char* outc = new char[out.size()+1];
			memcpy(outc, out.c_str(), out.size()+1);
			return outc;
		}

		unsigned int ReadUint32()
		{
			m_pos+=4;
			return *(unsigned int*)(m_buf+m_pos-4);
		}

		unsigned int Tell()
		{
			return m_pos;
		}

		void Seek(unsigned int pos)
		{
			m_pos = pos;
		}

		char* GetBuf()
		{
			return m_buf+m_pos;
		}
};

extern "C"
{
	void initlibp3dtoolconfig();
	void initunicodedata();
	void initlibpandaexpress();
	void initlibpanda();
	void initlibpandaegg();
	void initlibpandaphysics();
	void initlibpandafx();
	void initlibp3direct();
	void initlibp3vision();
	void initlibp3skel();
	void init_socket();
	void initlibpandaode();
}
void init_libpandagl();
void init_libpnmimagetypes();
void init_libOpenALAudio();

#ifdef _DEBUG
	#define DEBUGLIB(x) x "_d.lib"
#else
	#define DEBUGLIB(x) x ".lib"
#endif

//These will be cleaned up later
#pragma comment(lib, DEBUGLIB("unicodedata"))
#pragma comment(lib, DEBUGLIB("libp3dtool"))
#pragma comment(lib, DEBUGLIB("libp3dtoolconfig"))
#pragma comment(lib, DEBUGLIB("libpandaexpress"))
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, DEBUGLIB("libpanda"))
#pragma comment(lib, DEBUGLIB("libpandaegg"))
#pragma comment(lib, DEBUGLIB("libpandagl"))
#pragma comment(lib, DEBUGLIB("libpandaphysics"))
#pragma comment(lib, DEBUGLIB("libpandafx"))
#pragma comment(lib, DEBUGLIB("libp3direct"))
#pragma comment(lib, DEBUGLIB("libp3vision"))
#pragma comment(lib, "opengl32.lib")
#pragma comment(lib, DEBUGLIB("libp3windisplay"))
#pragma comment(lib, "Imm32.lib")
#pragma comment(lib, DEBUGLIB("libp3openal_audio"))
#pragma comment(lib, DEBUGLIB("libp3skel"))
#pragma comment(lib, "C:\\repos\\mirai\\panda3d-1.8.1\\thirdparty\\win-libs-vc9\\png\\lib\\libpandapng.lib")
#pragma comment(lib, "C:\\repos\\mirai\\panda3d-1.8.1\\thirdparty\\win-libs-vc9\\jpeg\\lib\\libpandajpeg.lib")
#pragma comment(lib, "C:\\repos\\mirai\\panda3d-1.8.1\\thirdparty\\win-libs-vc9\\nvidiacg\\lib\\cg.lib")
#pragma comment(lib, "C:\\repos\\mirai\\panda3d-1.8.1\\thirdparty\\win-libs-vc9\\nvidiacg\\lib\\cgGL.lib")
#pragma comment(lib, "C:\\repos\\mirai\\panda3d-1.8.1\\thirdparty\\win-libs-vc9\\openal\\lib\\OpenAL32.lib")
#pragma comment(lib, "C:\\openssl\\lib\\libeay32.lib")
#pragma comment(lib, "C:\\openssl\\lib\\ssleay32.lib")
#pragma comment(lib, "C:\\freetype\\objs\\win32\\vc2010\\freetype2411.lib")
#pragma comment(lib, DEBUGLIB("_socket"))
#pragma comment(lib, DEBUGLIB("libpandaode"))
#pragma comment(lib, "C:\\ode-0.12\\lib\\ReleaseDoubleLib\\ode_double.lib")
#pragma comment(lib, "C:\\libvorbis-1.3.3\\win32\\VS2010\\Win32\\Release\\libvorbisfile_static.lib")
#pragma comment(lib, "C:\\libvorbis-1.3.3\\win32\\VS2010\\Win32\\Release\\libvorbis_static.lib")

std::string decrypt(const std::string &input, const std::string &key)
{
	std::string output;
	output.reserve(input.length());
	for(unsigned int i = 0; i < input.size(); ++i)
	{
		unsigned char k = key[i&key.length()];
		unsigned char c = input[i];
		c = ((c&0x0F)<<4) | ((c&0xF0)>>4);
		c = (~c) ^ k;
		output += c;
	}
	return output;
}

int main(int argc, char* argv[])
{
	Py_DontWriteBytecodeFlag = 1;
	Py_NoSiteFlag = 1;
	//Py_VerboseFlag = 1;
	#ifdef _DEBUG
		if(argc > 1)
		{
			Py_Initialize();
			initunicodedata();
			init_socket();
			initlibpandaexpress();
			initlibpanda();
			init_libpnmimagetypes();
			initlibpandaegg();
			init_libpandagl();
			initlibpandaphysics();
			initlibpandafx();
			initlibp3direct();
			initlibp3vision();
			initlibp3skel();
			initlibpandaode();
			PyRun_SimpleString(
				"import sys\n"
				"sys.path.append('C:\\python27\\Lib')\n"
				"sys.path.append('C:\\repos\\mirai\\p3dbuild\\lib')\n"
				"import site\n"
			);
			Py_Main(argc, argv);
			return 0;
		}
	#endif
	
	std::cout << "Reading game blob." << std::endl;
	std::fstream gameBlob;
	gameBlob.open("TTRGame.bin", std::ios_base::in | std::ios_base::binary);
	if(!gameBlob.is_open())
	{
		//TODO: ERROR string
		exit(1);
	}
	gameBlob.seekg(0, std::ios_base::end);
	size_t size = gameBlob.tellg();
	gameBlob.seekg(0, std::ios_base::beg);
	char *data = new char[size];
	gameBlob.read(data, size);
	gameBlob.close();
	unsigned char iv[16];
	memset(iv, 0, 16);

	std::cout << "Decrypting game blob" << std::endl;
	EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
	EVP_CIPHER_CTX_init(ctx);
	EVP_DecryptInit(ctx, EVP_aes_128_cbc(), 
		(unsigned char*)decrypt("\x37\xCE\x5C\xDB\xF8\x96\xC3\xE4\x9A\x24\xA9\x8A\xC1\x7E\xF6\xEF", 
		"\x98\xF1\x94\x92\x19\x74\x43\x24\xCA\x6D\x74\x7F\x2A\x30\xB9\x3F").c_str(), iv);
	int junk;
	EVP_DecryptUpdate(ctx, (unsigned char*)data, &junk, (unsigned char*)data, size);
	EVP_DecryptFinal(ctx, (unsigned char*)(data+junk), &junk);
	EVP_CIPHER_CTX_cleanup(ctx);
	EVP_CIPHER_CTX_free(ctx);

	Reader rdr(data, size);
	
	std::cout << "Freezing modules" << std::endl;
	std::vector<_frozen> modules;
	while(rdr.Tell() < size)
	{
		//std::cout << "Seeking past IV" << std::endl;
		rdr.Seek(rdr.Tell()+16);
		//std::cout << "Reading name" << std::endl;
		char* name = rdr.ReadCString();
		if(name[0] == 0)
		{
			break;
		}
		//std::cout << "Name is: " << name << std::endl;
		int codeSize = rdr.ReadUint32();
		//std::cout << "Reading code size" << std::endl;
		bool package = false;
		if(codeSize < 0)
		{
			package = true;
			codeSize *= -1;
		}
		char* code = new char[codeSize];
		memcpy(code, rdr.GetBuf(), codeSize);
		//std::cout << "Reading code" << std::endl;
		rdr.Seek(rdr.Tell()+codeSize);
		//std::cout << "Putting module into vector" << std::endl;
		unsigned int mn = modules.size();
		modules.resize(modules.size()+1);
		modules[mn].name = name;
		modules[mn].code = (unsigned char*)code;
		modules[mn].size = codeSize*(package ? -1 : 1);
		if(rdr.Tell()%16)
		{
			rdr.Seek(rdr.Tell()+(16-(rdr.Tell()%16)));
		}
	}

	std::cout << "Copying vector to array of _frozen" << std::endl;
	_frozen *fzns = new _frozen[modules.size()+1];
	for(unsigned int i = 0; i < modules.size(); ++i)
	{
		memcpy(&fzns[i], &modules[i], sizeof(_frozen));
	}
	memset(&fzns[modules.size()], 0, sizeof(_frozen));
	PyImport_FrozenModules = fzns;

	std::cout << "Initializing python" << std::endl;
	Py_Initialize();
	initunicodedata();
	init_socket();
	initlibp3dtoolconfig();
	PyImport_ImportFrozenModule("__config__");
	initlibpandaexpress();
	initlibpanda();
	init_libpnmimagetypes();
	initlibpandaegg();
	init_libpandagl();
	initlibpandaphysics();
	initlibpandafx();
	initlibp3direct();
	initlibp3vision();
	initlibp3skel();
	initlibpandaode();
	std::cout << "Starting game" << std::endl;
	PyImport_ImportFrozenModule("__main__");
	PyErr_Print();
	return 0;
}

