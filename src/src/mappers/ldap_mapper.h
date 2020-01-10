/*
 * PAM-PKCS11 mapping modules
 * Copyright (C) 2005 Juan Antonio Martinez <jonsito@teleline.es>
 * pam-pkcs11 is copyright (C) 2003-2004 of Mario Strasser <mast@gmx.net>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 *
 * $Id: ldap_mapper.h 358 2008-11-06 14:28:46Z ludovic.rousseau $
 */

#ifndef __LDAP_MAPPER_H_
#define __LDAP_MAPPER_H_

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "../scconf/scconf.h"
#include "mapper.h"

#ifdef LDAP_MAPPER_STATIC

#ifndef __LDAP_MAPPER_C_
#define LDAP_EXTERN extern
#else
#define LDAP_EXTERN
#endif
LDAP_EXTERN mapper_module * ldap_mapper_module_init(scconf_block *blk,const char *mapper_name);
#undef LDAP_EXTERN

/* end of static (if any) declarations */
#endif

/* End of ldap_mapper.h */
#endif
