 # https://github.com/samba-team/samba/blob/7a662e097be5e0d3f7779fa544486968b8f57063/source4/smb_server/smb/receive.c#L90

smbsrv_reply_printopen = "smbsrv_reply_printopen"
smbsrv_reply_printwrite = "smbsrv_reply_printwrite"
smbsrv_reply_printclose = "smbsrv_reply_printclose"
smbsrv_reply_printqueue = "smbsrv_reply_printqueue"
smbsrv_reply_ntrename = "smbsrv_reply_ntrename"
smbsrv_reply_ntcancel = "smbsrv_reply_ntcancel"
smbsrv_reply_ntcreate_and_X = "smbsrv_reply_ntcreate_and_X"
smbsrv_reply_nttranss = "smbsrv_reply_nttranss"
smbsrv_reply_nttrans = "smbsrv_reply_nttrans"
smbsrv_reply_fclose = "smbsrv_reply_fclose"
smbsrv_reply_search= "smbsrv_reply_search"
smbsrv_reply_dskattr= "smbsrv_reply_dskattr"
smbsrv_reply_tcon_and_X= "smbsrv_reply_tcon_and_X"
smbsrv_reply_sesssetup= "smbsrv_reply_sesssetup"
smbsrv_reply_ulogoffX= "smbsrv_reply_ulogoffX"
smbsrv_reply_negprot= "smbsrv_reply_negprot"
smbsrv_reply_tdis= "smbsrv_reply_tdis"
smbsrv_reply_tcon= "smbsrv_reply_tcon"
smbsrv_reply_findnclose= "smbsrv_reply_findnclose"
smbsrv_reply_findclose= "smbsrv_reply_findclose"
smbsrv_reply_transs2= "smbsrv_reply_transs2"
smbsrv_reply_trans2= "smbsrv_reply_trans2"
smbsrv_reply_write_and_X= "smbsrv_reply_write_and_X"
smbsrv_reply_read_and_X= "smbsrv_reply_read_and_X"
smbsrv_reply_open_and_X= "smbsrv_reply_open_and_X"
smbsrv_reply_writeclose= "smbsrv_reply_writeclose"
smbsrv_reply_echo= "smbsrv_reply_echo"
smbsrv_reply_copy= "smbsrv_reply_copy"
smbsrv_reply_ioctl= "smbsrv_reply_ioctl"
smbsrv_reply_transs= "smbsrv_reply_transs"
smbsrv_reply_trans= "smbsrv_reply_trans"
smbsrv_reply_lockingX= "smbsrv_reply_lockingX"
smbsrv_reply_getattrE = "smbsrv_reply_getattrE"
smbsrv_reply_setattrE = "smbsrv_reply_setattrE"
smbsrv_reply_writebs= "smbsrv_reply_writebs"
smbsrv_reply_writebmpx= "smbsrv_reply_writebmpx"
smbsrv_reply_writebraw= "smbsrv_reply_writebraw"
smbsrv_reply_readbmpx= "smbsrv_reply_readbmpx"
smbsrv_reply_readbraw= "smbsrv_reply_readbraw"
smbsrv_reply_writeunlock= "smbsrv_reply_writeunlock"
smbsrv_reply_lockread= "smbsrv_reply_lockread"
smbsrv_reply_lseek= "smbsrv_reply_lseek"
smbsrv_reply_exit= "smbsrv_reply_exit"
smbsrv_reply_chkpth= "smbsrv_reply_chkpth"
smbsrv_reply_mknew= "smbsrv_reply_mknew"
smbsrv_reply_ctemp= "smbsrv_reply_ctemp"
smbsrv_reply_unlock= "smbsrv_reply_unlock"
smbsrv_reply_lock= "smbsrv_reply_lock"
smbsrv_reply_write= "smbsrv_reply_write"
smbsrv_reply_read= "smbsrv_reply_read"
smbsrv_reply_setatr= "smbsrv_reply_setatr"
smbsrv_reply_getatr= "smbsrv_reply_getatr"
smbsrv_reply_mv= "smbsrv_reply_mv"
smbsrv_reply_unlink= "smbsrv_reply_unlink"
smbsrv_reply_flush= "smbsrv_reply_flush"
smbsrv_reply_close= "smbsrv_reply_close"
smbsrv_reply_open = "smbsrv_reply_open"
smbsrv_reply_rmdir = "smbsrv_reply_rmdir"
smbsrv_reply_mkdir = "smbsrv_reply_mkdir"






NEED_SESS = 0x00001
NEED_TCON = 0x00010
SIGNING_NO_REPLY = 0x00100
AND_X = 0x01000
LARGE_REQUEST = 0x10000

smb_messages = [
# 0x00
 [ "SMBmkdir",	smbsrv_reply_mkdir,		NEED_SESS|NEED_TCON ],
# 0x01
 [ "SMBrmdir",	smbsrv_reply_rmdir,		NEED_SESS|NEED_TCON ],
# 0x02
 [ "SMBopen",		smbsrv_reply_open,		NEED_SESS|NEED_TCON ],
# 0x03
 [ "SMBcreate",	smbsrv_reply_mknew,		NEED_SESS|NEED_TCON ],
# 0x04
 [ "SMBclose",	smbsrv_reply_close,		NEED_SESS|NEED_TCON ],
# 0x05
 [ "SMBflush",	smbsrv_reply_flush,		NEED_SESS|NEED_TCON ],
# 0x06
 [ "SMBunlink",	smbsrv_reply_unlink,		NEED_SESS|NEED_TCON ],
# 0x07
 [ "SMBmv",		smbsrv_reply_mv,		NEED_SESS|NEED_TCON ],
# 0x08
 [ "SMBgetatr",	smbsrv_reply_getatr,		NEED_SESS|NEED_TCON ],
# 0x09
 [ "SMBsetatr",	smbsrv_reply_setatr,		NEED_SESS|NEED_TCON ],
# 0x0a
 [ "SMBread",		smbsrv_reply_read,		NEED_SESS|NEED_TCON ],
# 0x0b
 [ "SMBwrite",	smbsrv_reply_write,		NEED_SESS|NEED_TCON ],
# 0x0c
 [ "SMBlock",		smbsrv_reply_lock,		NEED_SESS|NEED_TCON ],
# 0x0d
 [ "SMBunlock",	smbsrv_reply_unlock,		NEED_SESS|NEED_TCON ],
# 0x0e
 [ "SMBctemp",	smbsrv_reply_ctemp,		NEED_SESS|NEED_TCON ],
# 0x0f
 [ "SMBmknew",	smbsrv_reply_mknew,		NEED_SESS|NEED_TCON ],
# 0x10
 [ "SMBcheckpath",	smbsrv_reply_chkpth,		NEED_SESS|NEED_TCON ],
# 0x11
 [ "SMBexit",		smbsrv_reply_exit,		NEED_SESS ],
# 0x12
 [ "SMBlseek",	smbsrv_reply_lseek,		NEED_SESS|NEED_TCON ],
# 0x13
 [ "SMBlockread",	smbsrv_reply_lockread,		NEED_SESS|NEED_TCON ],
# 0x14
 [ "SMBwriteunlock",	smbsrv_reply_writeunlock,	NEED_SESS|NEED_TCON ],
# 0x15
 [ None, None, 0 ],
# 0x16
 [ None, None, 0 ],
# 0x17
 [ None, None, 0 ],
# 0x18
 [ None, None, 0 ],
# 0x19
 [ None, None, 0 ],
# 0x1a
 [ "SMBreadbraw",	smbsrv_reply_readbraw,		NEED_SESS|NEED_TCON ],
# 0x1b
 [ "SMBreadBmpx",	smbsrv_reply_readbmpx,		NEED_SESS|NEED_TCON ],
# 0x1c
 [ "SMBreadBs",	None,				0 ],
# 0x1d
 [ "SMBwritebraw",	smbsrv_reply_writebraw,		NEED_SESS|NEED_TCON ],
# 0x1e
 [ "SMBwriteBmpx",	smbsrv_reply_writebmpx,		NEED_SESS|NEED_TCON ],
# 0x1f
 [ "SMBwriteBs",	smbsrv_reply_writebs,		NEED_SESS|NEED_TCON ],
# 0x20
 [ "SMBwritec",	None,				0 ],
# 0x21
 [ None, None, 0 ],
# 0x22
 [ "SMBsetattrE",	smbsrv_reply_setattrE,		NEED_SESS|NEED_TCON ],
# 0x23
 [ "SMBgetattrE",	smbsrv_reply_getattrE,		NEED_SESS|NEED_TCON ],
# 0x24
 [ "SMBlockingX",	smbsrv_reply_lockingX,		NEED_SESS|NEED_TCON|AND_X ],
# 0x25
 [ "SMBtrans",	smbsrv_reply_trans,		NEED_SESS|NEED_TCON ],
# 0x26
 [ "SMBtranss",	smbsrv_reply_transs,		NEED_SESS|NEED_TCON ],
# 0x27
 [ "SMBioctl",	smbsrv_reply_ioctl,		NEED_SESS|NEED_TCON ],
# 0x28
 [ "SMBioctls",	None,				NEED_SESS|NEED_TCON ],
# 0x29
 [ "SMBcopy",		smbsrv_reply_copy,		NEED_SESS|NEED_TCON ],
# 0x2a
 [ "SMBmove",		None,				NEED_SESS|NEED_TCON ],
# 0x2b
 [ "SMBecho",		smbsrv_reply_echo,		0 ],
# 0x2c
 [ "SMBwriteclose",	smbsrv_reply_writeclose,	NEED_SESS|NEED_TCON ],
# 0x2d
 [ "SMBopenX",	smbsrv_reply_open_and_X,	NEED_SESS|NEED_TCON|AND_X ],
# 0x2e
 [ "SMBreadX",	smbsrv_reply_read_and_X,	NEED_SESS|NEED_TCON|AND_X ],
# 0x2f
 [ "SMBwriteX",	smbsrv_reply_write_and_X,	NEED_SESS|NEED_TCON|AND_X|LARGE_REQUEST],
# 0x30
 [ None, None, 0 ],
# 0x31
 [ None, None, 0 ],
# 0x32
 [ "SMBtrans2",	smbsrv_reply_trans2,		NEED_SESS|NEED_TCON ],
# 0x33
 [ "SMBtranss2",	smbsrv_reply_transs2,		NEED_SESS|NEED_TCON ],
# 0x34
 [ "SMBfindclose",	smbsrv_reply_findclose,		NEED_SESS|NEED_TCON ],
# 0x35
 [ "SMBfindnclose",	smbsrv_reply_findnclose,	NEED_SESS|NEED_TCON ],
# 0x36
 [ None, None, 0 ],
# 0x37
 [ None, None, 0 ],
# 0x38
 [ None, None, 0 ],
# 0x39
 [ None, None, 0 ],
# 0x3a
 [ None, None, 0 ],
# 0x3b
 [ None, None, 0 ],
# 0x3c
 [ None, None, 0 ],
# 0x3d
 [ None, None, 0 ],
# 0x3e
 [ None, None, 0 ],
# 0x3f
 [ None, None, 0 ],
# 0x40
 [ None, None, 0 ],
# 0x41
 [ None, None, 0 ],
# 0x42
 [ None, None, 0 ],
# 0x43
 [ None, None, 0 ],
# 0x44
 [ None, None, 0 ],
# 0x45
 [ None, None, 0 ],
# 0x46
 [ None, None, 0 ],
# 0x47
 [ None, None, 0 ],
# 0x48
 [ None, None, 0 ],
# 0x49
 [ None, None, 0 ],
# 0x4a
 [ None, None, 0 ],
# 0x4b
 [ None, None, 0 ],
# 0x4c
 [ None, None, 0 ],
# 0x4d
 [ None, None, 0 ],
# 0x4e
 [ None, None, 0 ],
# 0x4f
 [ None, None, 0 ],
# 0x50
 [ None, None, 0 ],
# 0x51
 [ None, None, 0 ],
# 0x52
 [ None, None, 0 ],
# 0x53
 [ None, None, 0 ],
# 0x54
 [ None, None, 0 ],
# 0x55
 [ None, None, 0 ],
# 0x56
 [ None, None, 0 ],
# 0x57
 [ None, None, 0 ],
# 0x58
 [ None, None, 0 ],
# 0x59
 [ None, None, 0 ],
# 0x5a
 [ None, None, 0 ],
# 0x5b
 [ None, None, 0 ],
# 0x5c
 [ None, None, 0 ],
# 0x5d
 [ None, None, 0 ],
# 0x5e
 [ None, None, 0 ],
# 0x5f
 [ None, None, 0 ],
# 0x60
 [ None, None, 0 ],
# 0x61
 [ None, None, 0 ],
# 0x62
 [ None, None, 0 ],
# 0x63
 [ None, None, 0 ],
# 0x64
 [ None, None, 0 ],
# 0x65
 [ None, None, 0 ],
# 0x66
 [ None, None, 0 ],
# 0x67
 [ None, None, 0 ],
# 0x68
 [ None, None, 0 ],
# 0x69
 [ None, None, 0 ],
# 0x6a
 [ None, None, 0 ],
# 0x6b
 [ None, None, 0 ],
# 0x6c
 [ None, None, 0 ],
# 0x6d
 [ None, None, 0 ],
# 0x6e
 [ None, None, 0 ],
# 0x6f
 [ None, None, 0 ],
# 0x70
 [ "SMBtcon",		smbsrv_reply_tcon,		NEED_SESS ],
# 0x71
 [ "SMBtdis",		smbsrv_reply_tdis,		NEED_TCON ],
# 0x72
 [ "SMBnegprot",	smbsrv_reply_negprot,		0 ],
# 0x73
 [ "SMBsesssetupX",	smbsrv_reply_sesssetup,		AND_X ],
# 0x74
 [ "SMBulogoffX",	smbsrv_reply_ulogoffX,		NEED_SESS|AND_X ], # ulogoff doesn't give a valid TID

# 0x75
 [ "SMBtconX",	smbsrv_reply_tcon_and_X,	NEED_SESS|AND_X ],
# 0x76
 [ None, None, 0 ],
# 0x77
 [ None, None, 0 ],
# 0x78
 [ None, None, 0 ],
# 0x79
 [ None, None, 0 ],
# 0x7a
 [ None, None, 0 ],
# 0x7b
 [ None, None, 0 ],
# 0x7c
 [ None, None, 0 ],
# 0x7d
 [ None, None, 0 ],
# 0x7e
 [ None, None, 0 ],
# 0x7f
 [ None, None, 0 ],
# 0x80
 [ "SMBdskattr",	smbsrv_reply_dskattr,		NEED_SESS|NEED_TCON ],
# 0x81
 [ "SMBsearch",	smbsrv_reply_search,		NEED_SESS|NEED_TCON ],
# 0x82
 [ "SMBffirst",	smbsrv_reply_search,		NEED_SESS|NEED_TCON ],
# 0x83
 [ "SMBfunique",	smbsrv_reply_search,		NEED_SESS|NEED_TCON ],
# 0x84
 [ "SMBfclose",	smbsrv_reply_fclose,		NEED_SESS|NEED_TCON ],
# 0x85
 [ None, None, 0 ],
# 0x86
 [ None, None, 0 ],
# 0x87
 [ None, None, 0 ],
# 0x88
 [ None, None, 0 ],
# 0x89
 [ None, None, 0 ],
# 0x8a
 [ None, None, 0 ],
# 0x8b
 [ None, None, 0 ],
# 0x8c
 [ None, None, 0 ],
# 0x8d
 [ None, None, 0 ],
# 0x8e
 [ None, None, 0 ],
# 0x8f
 [ None, None, 0 ],
# 0x90
 [ None, None, 0 ],
# 0x91
 [ None, None, 0 ],
# 0x92
 [ None, None, 0 ],
# 0x93
 [ None, None, 0 ],
# 0x94
 [ None, None, 0 ],
# 0x95
 [ None, None, 0 ],
# 0x96
 [ None, None, 0 ],
# 0x97
 [ None, None, 0 ],
# 0x98
 [ None, None, 0 ],
# 0x99
 [ None, None, 0 ],
# 0x9a
 [ None, None, 0 ],
# 0x9b
 [ None, None, 0 ],
# 0x9c
 [ None, None, 0 ],
# 0x9d
 [ None, None, 0 ],
# 0x9e
 [ None, None, 0 ],
# 0x9f
 [ None, None, 0 ],
# 0xa0
 [ "SMBnttrans",	smbsrv_reply_nttrans,		NEED_SESS|NEED_TCON|LARGE_REQUEST ],
# 0xa1
 [ "SMBnttranss",	smbsrv_reply_nttranss,		NEED_SESS|NEED_TCON ],
# 0xa2
 [ "SMBntcreateX",	smbsrv_reply_ntcreate_and_X,	NEED_SESS|NEED_TCON|AND_X ],
# 0xa3
 [ None, None, 0 ],
# 0xa4
 [ "SMBntcancel",	smbsrv_reply_ntcancel,		NEED_SESS|NEED_TCON|SIGNING_NO_REPLY ],
# 0xa5
 [ "SMBntrename",	smbsrv_reply_ntrename,		NEED_SESS|NEED_TCON ],
# 0xa6
 [ None, None, 0 ],
# 0xa7
 [ None, None, 0 ],
# 0xa8
 [ None, None, 0 ],
# 0xa9
 [ None, None, 0 ],
# 0xaa
 [ None, None, 0 ],
# 0xab
 [ None, None, 0 ],
# 0xac
 [ None, None, 0 ],
# 0xad
 [ None, None, 0 ],
# 0xae
 [ None, None, 0 ],
# 0xaf
 [ None, None, 0 ],
# 0xb0
 [ None, None, 0 ],
# 0xb1
 [ None, None, 0 ],
# 0xb2
 [ None, None, 0 ],
# 0xb3
 [ None, None, 0 ],
# 0xb4
 [ None, None, 0 ],
# 0xb5
 [ None, None, 0 ],
# 0xb6
 [ None, None, 0 ],
# 0xb7
 [ None, None, 0 ],
# 0xb8
 [ None, None, 0 ],
# 0xb9
 [ None, None, 0 ],
# 0xba
 [ None, None, 0 ],
# 0xbb
 [ None, None, 0 ],
# 0xbc
 [ None, None, 0 ],
# 0xbd
 [ None, None, 0 ],
# 0xbe
 [ None, None, 0 ],
# 0xbf
 [ None, None, 0 ],
# 0xc0
 [ "SMBsplopen",	smbsrv_reply_printopen,		NEED_SESS|NEED_TCON ],
# 0xc1
 [ "SMBsplwr",	smbsrv_reply_printwrite,	NEED_SESS|NEED_TCON ],
# 0xc2
 [ "SMBsplclose",	smbsrv_reply_printclose,	NEED_SESS|NEED_TCON ],
# 0xc3
 [ "SMBsplretq",	smbsrv_reply_printqueue,	NEED_SESS|NEED_TCON ],
# 0xc4
 [ None, None, 0 ],
# 0xc5
 [ None, None, 0 ],
# 0xc6
 [ None, None, 0 ],
# 0xc7
 [ None, None, 0 ],
# 0xc8
 [ None, None, 0 ],
# 0xc9
 [ None, None, 0 ],
# 0xca
 [ None, None, 0 ],
# 0xcb
 [ None, None, 0 ],
# 0xcc
 [ None, None, 0 ],
# 0xcd
 [ None, None, 0 ],
# 0xce
 [ None, None, 0 ],
# 0xcf
 [ None, None, 0 ],
# 0xd0
 [ "SMBsends",	None,				0 ],
# 0xd1
 [ "SMBsendb",	None,				0 ],
# 0xd2
 [ "SMBfwdname",	None,				0 ],
# 0xd3
 [ "SMBcancelf",	None,				0 ],
# 0xd4
 [ "SMBgetmac",	None,				0 ],
# 0xd5
 [ "SMBsendstrt",	None,				0 ],
# 0xd6
 [ "SMBsendend",	None,				0 ],
# 0xd7
 [ "SMBsendtxt",	None,				0 ],
# 0xd8
 [ None, None, 0 ],
# 0xd9
 [ None, None, 0 ],
# 0xda
 [ None, None, 0 ],
# 0xdb
 [ None, None, 0 ],
# 0xdc
 [ None, None, 0 ],
# 0xdd
 [ None, None, 0 ],
# 0xde
 [ None, None, 0 ],
# 0xdf
 [ None, None, 0 ],
# 0xe0
 [ None, None, 0 ],
# 0xe1
 [ None, None, 0 ],
# 0xe2
 [ None, None, 0 ],
# 0xe3
 [ None, None, 0 ],
# 0xe4
 [ None, None, 0 ],
# 0xe5
 [ None, None, 0 ],
# 0xe6
 [ None, None, 0 ],
# 0xe7
 [ None, None, 0 ],
# 0xe8
 [ None, None, 0 ],
# 0xe9
 [ None, None, 0 ],
# 0xea
 [ None, None, 0 ],
# 0xeb
 [ None, None, 0 ],
# 0xec
 [ None, None, 0 ],
# 0xed
 [ None, None, 0 ],
# 0xee
 [ None, None, 0 ],
# 0xef
 [ None, None, 0 ],
# 0xf0
 [ None, None, 0 ],
# 0xf1
 [ None, None, 0 ],
# 0xf2
 [ None, None, 0 ],
# 0xf3
 [ None, None, 0 ],
# 0xf4
 [ None, None, 0 ],
# 0xf5
 [ None, None, 0 ],
# 0xf6
 [ None, None, 0 ],
# 0xf7
 [ None, None, 0 ],
# 0xf8
 [ None, None, 0 ],
# 0xf9
 [ None, None, 0 ],
# 0xfa
 [ None, None, 0 ],
# 0xfb
 [ None, None, 0 ],
# 0xfc
 [ None, None, 0 ],
# 0xfd
 [ None, None, 0 ],
# 0xfe
 [ None, None, 0 ],
# 0xff
 [ None, None, 0 ]
]








##################################################
#########################
######################### Defining const values, source:
######################### https://github.com/samba-team/samba/blob/7a662e097be5e0d3f7779fa544486968b8f57063/libcli/smb/smb_constants.h#L22
#########################
##################################################


NBSSmessage = 0x00  # session message
NBSSrequest = 0x81  # session request
NBSSpositive = 0x82  # positive session response
NBSSnegative = 0x83  # negative session response
NBSSretarget = 0x84  # retarget session response
NBSSkeepalive = 0x85  # keepalive

SMB_MAGIC = 0x424D53FF  # 0xFF 'S' 'M' 'B'

# todo SMB2
SMB2_MAGIC = 0x424D53FE  # 0xFE 'S' 'M' 'B'

# the basic packet size, assuming no words or bytes. Does not include the NBT header
MIN_SMB_SIZE = 35

# when using NBT encapsulation every packet has a 4 byte header
NBT_HDR_SIZE = 4

# offsets into message header for common items - NOTE: These have
# changed from being offsets from the base of the NBT packet to the base of the SMB packet.
# this has reduced all these values by 4

HDR_COM = 4
HDR_RCLS = 5
HDR_REH = 6
HDR_ERR = 7
HDR_FLG = 9
HDR_FLG2 = 10
HDR_PIDHIGH = 12
HDR_SS_FIELD = 14
HDR_TID = 24
HDR_PID = 26
HDR_UID = 28
HDR_MID = 30
HDR_WCT = 32
HDR_VWV = 33

