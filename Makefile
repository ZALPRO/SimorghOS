# سیمرغ‌اواس — اهداف ساخت
.PHONY: iso clean test lint

iso:
	sudo -E ./build.sh

test:
	python3 tools/test_jalaali.py

lint:
	python3 -m py_compile tools/jalaali.py config/includes.chroot/usr/share/simorgh/jalaali.py
	python3 -m py_compile config/includes.chroot/usr/share/simorgh/bin/simorgh-jdate
	bash -n config/includes.chroot/usr/share/simorgh/bin/simorgh-set-theme
	bash -n config/includes.chroot/usr/share/simorgh/bin/simorgh
	bash -n config/includes.chroot/usr/share/simorgh/bin/simorgh-center
	bash -n config/includes.chroot/usr/share/simorgh/bin/simorgh-store
	bash -n scripts/install-simorgh.sh build.sh
	@echo lint OK

clean:
	sudo -E ./build.sh clean
