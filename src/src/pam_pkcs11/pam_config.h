/*
 * PKCS #11 PAM Login Module
 * Copyright (C) 2003 Mario Strasser <mast@gmx.net>,
 * config mgmt copyright (c) 2005 Juan Antonio Martinez <jonsito@teleline.es>
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
 * $Id: pam_config.h 341 2008-10-14 07:36:46Z ludovic.rousseau $
 */

/*
* configuration related functions
*/
#ifndef _PAM_CONFIG_H_
#define _PAM_CONFIG_H_

#include "../scconf/scconf.h"
#include "../common/cert_vfy.h"

struct configuration_st {
	char * config_file;
	scconf_context *ctx;
	int debug;
	int nullok;
	int try_first_pass;
	int use_first_pass;
	int use_authok;
	int card_only;
	int wait_for_card;
	char *pkcs11_module;
	char *pkcs11_modulepath;
	char **screen_savers;
	char *slot_description;
	int slot_num;
	int support_threads;
	cert_policy policy;
	char *token_type;
	char *username; /* provided user name */
};

struct configuration_st *pk_configure( int argc, const char **argv );

#endif
