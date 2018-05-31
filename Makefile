publish:
	jekyll build
	rsync -av --delete _site/* juan@gangas:/var/www/html/blog/