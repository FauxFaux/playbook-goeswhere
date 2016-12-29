root /opt/phabricator/phabricator/webroot;

client_max_body_size 10m;

location / {
  index index.php;
  rewrite ^/(.*)$ /index.php?__path__=/$1 last;
}

location = /favicon.ico {
  try_files $uri =204;
}

location /index.php {
  fastcgi_pass    unix:/var/run/php-fpm-phab.sock;
  fastcgi_index   index.php;

  #required if PHP was built with --enable-force-cgi-redirect
  fastcgi_param  REDIRECT_STATUS    200;

  #variables to make the $_SERVER populate in PHP
  fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;
  fastcgi_param  QUERY_STRING       $query_string;
  fastcgi_param  REQUEST_METHOD     $request_method;
  fastcgi_param  CONTENT_TYPE       $content_type;
  fastcgi_param  CONTENT_LENGTH     $content_length;

  fastcgi_param  SCRIPT_NAME        $fastcgi_script_name;

  fastcgi_param  GATEWAY_INTERFACE  CGI/1.1;
  fastcgi_param  SERVER_SOFTWARE    nginx/$nginx_version;

  fastcgi_param  REMOTE_ADDR        $remote_addr;
}
