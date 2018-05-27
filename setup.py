import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from shutil import rmtree
from subprocess import call

from distutils import log


class pushd(object):

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, type_, value, traceback):
        os.chdir(self.saved_path)


class generate_files_mixin(object):

    here = os.path.abspath(os.path.dirname(__file__))

    ccdir = "cookieconsent"
    nodemoddir = os.path.join(ccdir, "node_modules")
    gulpbin = os.path.join(here, nodemoddir, ".bin", "gulp")

    ccbuilddir = os.path.join(ccdir, "build")

    pymodroot = os.path.join("tw2", "cookieconsent")
    staticdir = os.path.join(pymodroot, "static")

    def generate_distribution(self):
        with pushd(self.ccdir):
            if not os.path.exists(self.gulpbin):
                log.info("Gulp missing...")
                log.info("\tInstalling nodejs modules")
                call(("npm", "install"))
                log.info("\tInstalling gulp")
                call(("npm", "install", "gulp"))
            log.info("Building distribution")
            call((self.gulpbin, "build"))

        log.info("Copying static files")
        topdepth = len(self.ccbuilddir.split(os.path.sep))
        if os.path.exists(self.staticdir):
            rmtree(self.staticdir)
        try:
            os.makedirs(self.staticdir)
        except OSError:
            pass

        for srcpath, dirs, files in os.walk(self.ccbuilddir):
            spcomps = srcpath.split(os.path.sep)
            destpath = os.path.join(self.staticdir, *spcomps[topdepth:])
            if not os.path.exists(destpath):
                os.mkdir(destpath)
            for f in files:
                sfpath = os.path.join(srcpath, f)
                dfpath = os.path.join(destpath, f)
                os.link(sfpath, dfpath)


class my_build_py(build_py, generate_files_mixin):

    def run(self):
        if not self.dry_run:
            self.generate_distribution()
        build_py.run(self)


class my_develop(develop, generate_files_mixin):

    def install_for_development(self):
        self.generate_distribution()
        develop.install_for_development(self)

    def uninstall_link(self):
        develop.uninstall_link(self)

        log.info("removing generated files: {}".format(self.staticdir))
        rmtree(self.staticdir)


def find_files(*paths_dirnames):
    all_files = set()

    for path, dirname in paths_dirnames:
        files = set()
        for dpath, dnames, fnames in os.walk(path):
            files.update(
                x for x in (os.path.join(dpath, y) for y in fnames)
                if os.path.isfile(x))
        cutchars = len(path)
        fnames = set(dirname + f[cutchars:] for f in files)
        all_files.update(fnames)

    return sorted(all_files)

if __name__ == '__main__':
    setup(
        name='tw2.cookieconsent',
        version='0.1',
        description="ToscaWidgets 2 wrapper for Silktide Cookie Consent",
        author="Nils Philippsen",
        author_email="nils@tiptoe.de",
        #url=
        #download_url=
        install_requires=["tw2.core >= 2.0", "speaklater"],
        packages=find_packages(),
        namespace_packages=['tw2'],
        zip_safe=False,
        include_package_data=True,
        #test_suite='nose.collector'
        package_data={'tw2.cookieconsent': find_files(
            ("tw2/cookieconsent/static", "static"))},
        entry_points="""
            [tw2.widgets]
            widgets = tw2.cookieconsent
        """,
        keywords=['tw2.widgets'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Web Environment",
            "Environment :: Web Environment :: ToscaWidgets",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Widget Sets",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
        ],
        cmdclass={
            'build_py': my_build_py,
            'develop': my_develop,
            }
    )
