#! /usr/bin/env python
# encoding: utf-8
# WARNING! All changes made to this file will be lost!

import re
from waflib import Utils
from waflib.Tools import fc,fc_config,fc_scan
from waflib.Configure import conf
def find_gfortran(conf):
	fc=conf.find_program('gfortran',var='FC')
	fc=conf.cmd_to_list(fc)
	conf.get_gfortran_version(fc)
	conf.env.FC_NAME='GFORTRAN'
def gfortran_flags(conf):
	v=conf.env
	v['FCFLAGS_fcshlib']=['-fPIC']
	v['FORTRANMODFLAG']=['-M','']
	v['FCFLAGS_DEBUG']=['-Werror']
def gfortran_modifier_win32(conf):
	fc_config.fortran_modifier_win32(conf)
def gfortran_modifier_cygwin(conf):
	fc_config.fortran_modifier_cygwin(conf)
def gfortran_modifier_darwin(conf):
	fc_config.fortran_modifier_darwin(conf)
def gfortran_modifier_platform(conf):
	dest_os=conf.env['DEST_OS']or Utils.unversioned_sys_platform()
	gfortran_modifier_func=getattr(conf,'gfortran_modifier_'+dest_os,None)
	if gfortran_modifier_func:
		gfortran_modifier_func()
def get_gfortran_version(conf,fc):
	version_re=re.compile(r"GNU\s*Fortran",re.I).search
	cmd=fc+['--version']
	out,err=fc_config.getoutput(conf,cmd,stdin=False)
	if out:match=version_re(out)
	else:match=version_re(err)
	if not match:
		conf.fatal('Could not determine the compiler type')
	cmd=fc+['-dM','-E','-']
	out,err=fc_config.getoutput(conf,cmd,stdin=True)
	if out.find('__GNUC__')<0:
		conf.fatal('Could not determine the compiler type')
	k={}
	out=out.split('\n')
	import shlex
	for line in out:
		lst=shlex.split(line)
		if len(lst)>2:
			key=lst[1]
			val=lst[2]
			k[key]=val
	def isD(var):
		return var in k
	def isT(var):
		return var in k and k[var]!='0'
	conf.env['FC_VERSION']=(k['__GNUC__'],k['__GNUC_MINOR__'],k['__GNUC_PATCHLEVEL__'])
def configure(conf):
	conf.find_gfortran()
	conf.find_ar()
	conf.fc_flags()
	conf.gfortran_flags()
	conf.gfortran_modifier_platform()

conf(find_gfortran)
conf(gfortran_flags)
conf(gfortran_modifier_win32)
conf(gfortran_modifier_cygwin)
conf(gfortran_modifier_darwin)
conf(gfortran_modifier_platform)
conf(get_gfortran_version)