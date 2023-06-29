from pythonforandroid.recipe import BootstrapNDKRecipe
from pythonforandroid.toolchain import Recipe, current_directory
from pythonforandroid.logger import info, debug, shprint, warning
from os.path import join, isdir, isfile
from os import environ
from multiprocessing import cpu_count
import sh
import glob


class Qt6Recipe(BootstrapNDKRecipe):
    name = 'qt6'
    version = '6.4.3'
    url = 'https://download.qt.io/archive/qt/6.4/{version}/single/qt-everywhere-src-{version}.zip'
    dir_name = 'qt6'

    built_libraries = {'dummy':'.'}

    depends = ['python3']
    conflicts = ['sdl2', 'genericndkbuild']
    # patches = ['add-way-to-disable-accessibility-env-var.patch']

    need_stl_shared = True


    # override as we can't statically define the libs due to arch in filename
    def get_libraries(self, arch_name, in_context=False):
        # TODO: don't hardcode, infer from build config
        self.built_libraries = {
            f'libQt5Core_{arch_name}.so': 'qtbase/lib',
            f'libQt5Gui_{arch_name}.so': 'qtbase/lib',
            f'libQt5Network_{arch_name}.so': 'qtbase/lib',
            f'libQt5Xml_{arch_name}.so': 'qtbase/lib',
            f'libQt5Concurrent_{arch_name}.so': 'qtbase/lib',
            f'libQt5Sql_{arch_name}.so': 'qtbase/lib',
            f'libQt5Qml_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QmlModels_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QmlWorkerScript_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5Quick_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QuickShapes_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QuickParticles_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QuickTemplates2_{arch_name}.so': 'qtquickcontrols2/lib',
            f'libQt5QuickControls2_{arch_name}.so': 'qtquickcontrols2/lib',
            f'libQt5RemoteObjects_{arch_name}.so': 'qtremoteobjects/lib',
            f'libQt5Multimedia_{arch_name}.so': 'qtmultimedia/lib',
            f'libQt5MultimediaQuick_{arch_name}.so': 'qtmultimedia/lib',
            f'libQt5Svg_{arch_name}.so': 'qtsvg/lib',
            f'libQt5VirtualKeyboard_{arch_name}.so': 'qtvirtualkeyboard/lib',
            f'libQt5AndroidExtras_{arch_name}.so': 'qtandroidextras/lib',

            f'libplugins_bearer_qandroidbearer_{arch_name}.so': 'qtbase/plugins/bearer',
            f'libplugins_platforms_qtforandroid_{arch_name}.so': 'qtbase/plugins/platforms',
            f'libplugins_imageformats_qjpeg_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qico_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qgif_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qtga_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qtiff_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qwebp_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qicns_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qwbmp_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qsvg_{arch_name}.so': 'qtsvg/plugins/imageformats',

            f'libplugins_iconengines_qsvgicon_{arch_name}.so': 'qtsvg/plugins/iconengines',

            f'libplugins_playlistformats_qtmultimedia_m3u_{arch_name}.so': 'qtmultimedia/plugins/playlistformats',
            f'libplugins_video_videonode_qtsgvideonode_android_{arch_name}.so': 'qtmultimedia/plugins/video/videonode',
            f'libplugins_mediaservice_qtmedia_android_{arch_name}.so': 'qtmultimedia/plugins/mediaservice',
            f'libplugins_audio_qtaudio_opensles_{arch_name}.so': 'qtmultimedia/plugins/audio',

            f'libplugins_platforminputcontexts_qtvirtualkeyboardplugin_{arch_name}.so': 'qtvirtualkeyboard/plugins/platforminputcontexts',
            f'libplugins_virtualkeyboard_qtvirtualkeyboard_hangul_{arch_name}.so': 'qtvirtualkeyboard/plugins/virtualkeyboard',
            f'libplugins_virtualkeyboard_qtvirtualkeyboard_openwnn_{arch_name}.so': 'qtvirtualkeyboard/plugins/virtualkeyboard',
            f'libplugins_virtualkeyboard_qtvirtualkeyboard_pinyin_{arch_name}.so': 'qtvirtualkeyboard/plugins/virtualkeyboard',
            f'libplugins_virtualkeyboard_qtvirtualkeyboard_tcime_{arch_name}.so': 'qtvirtualkeyboard/plugins/virtualkeyboard',
            f'libplugins_virtualkeyboard_qtvirtualkeyboard_thai_{arch_name}.so': 'qtvirtualkeyboard/plugins/virtualkeyboard',

            f'libplugins_qmltooling_qmldbg_preview_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_native_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_debugger_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_local_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_messages_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_quickprofiler_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_nativedebugger_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_server_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_tcp_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_inspector_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_profiler_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',

            f'libqml_QtQml_qmlplugin_{arch_name}.so': 'qtdeclarative/qml/QtQml',
            f'libqml_QtQml_WorkerScript.2_workerscriptplugin_{arch_name}.so': 'qtdeclarative/qml/QtQml/WorkerScript.2',
            f'libqml_QtQml_StateMachine_qtqmlstatemachine_{arch_name}.so': 'qtdeclarative/qml/QtQml/StateMachine',
            f'libqml_QtQml_Models.2_modelsplugin_{arch_name}.so': 'qtdeclarative/qml/QtQml/Models.2',
            f'libqml_QtQuick_Window.2_windowplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/Window.2',
            f'libqml_QtQuick_Layouts_qquicklayoutsplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/Layouts',
            f'libqml_QtQuick_Shapes_qmlshapesplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/Shapes',
            f'libqml_QtQuick.2_qtquick2plugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick.2',
            f'libqml_QtQuick_LocalStorage_qmllocalstorageplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/LocalStorage',
            f'libqml_QtQuick_Templates.2_qtquicktemplates2plugin_{arch_name}.so': 'qtquickcontrols2/qml/QtQuick/Templates.2',
            f'libqml_QtQuick_Controls.2_qtquickcontrols2plugin_{arch_name}.so': 'qtquickcontrols2/qml/QtQuick/Controls.2',
            f'libqml_QtQuick_Controls.2_Material_qqc2materialstyleplugin_{arch_name}.so': 'qtquickcontrols2/qml/QtQuick/Controls.2/Material',
            f'libqml_QtRemoteObjects_qtremoteobjects_{arch_name}.so': 'qtremoteobjects/qml/QtRemoteObjects',
            f'libqml_QtGraphicalEffects_qtgraphicaleffectsplugin_{arch_name}.so': 'qtgraphicaleffects/qml/QtGraphicalEffects',
            f'libqml_QtGraphicalEffects_private_qtgraphicaleffectsprivate_{arch_name}.so': 'qtgraphicaleffects/qml/QtGraphicalEffects/private',
            f'libqml_QtMultimedia_declarative_multimedia_{arch_name}.so': 'qtmultimedia/qml/QtMultimedia',

            f'libqml_Qt_labs_folderlistmodel_qmlfolderlistmodelplugin_{arch_name}.so': 'qtdeclarative/qml/Qt/labs/folderlistmodel',
            f'libqml_QtQuick_VirtualKeyboard_qtquickvirtualkeyboardplugin_{arch_name}.so': 'qtvirtualkeyboard/qml/QtQuick/VirtualKeyboard',
            f'libqml_QtQuick_VirtualKeyboard_Settings_qtquickvirtualkeyboardsettingsplugin_{arch_name}.so': 'qtvirtualkeyboard/qml/QtQuick/VirtualKeyboard/Settings',
            f'libqml_QtQuick_VirtualKeyboard_Styles_qtquickvirtualkeyboardstylesplugin_{arch_name}.so': 'qtvirtualkeyboard/qml/QtQuick/VirtualKeyboard/Styles',
        }
        return super().get_libraries(arch_name, in_context)

    def get_recipe_env(self, arch=None, with_flags_in_cc=True, with_python=True):
        env = super().get_recipe_env(
            arch=arch, with_flags_in_cc=with_flags_in_cc,
            with_python=with_python,
        )
        env['APP_ALLOW_MISSING_DEPS'] = 'true'
        # env['TARGET_QMAKEPATH'] = join(self.ctx.libs_dir, 'bin')

        return env

    def build_arch(self, arch):
        super().build_arch(arch)

        env = self.get_recipe_env(arch)
        with current_directory(self.get_jni_dir()):
            shprint(sh.Command(join(self.ctx.ndk_dir, "ndk-build")),
                    #"APP_ALLOW_MISSING_DEPS=true",
                    "V=1", _env=env, _critical=True)

        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            info("compiling qt6 from sources")
            debug("environment: {}".format(env))

            ndk_sysroot = join(self.ctx.ndk_dir, 'sysroot')
            info("NDK sysroot: %s" % ndk_sysroot)
            info("libdir: %s" % join(build_dir, 'obj', 'local', arch.arch))

            # wtf
            shprint(sh.Command('dos2unix'), 'configure')
            shprint(sh.Command('dos2unix'), 'qtbase/configure')

            configure = sh.Command('./configure')
            # options?
            shprint(configure, '--help', _env=env, _tail=50, _critical=True)

            configure = configure.bake('-opensource', '-confirm-license', '-disable-rpath')
            configure = configure.bake('-android-sdk', self.ctx.sdk_dir)
            configure = configure.bake('-android-ndk', self.ctx.ndk_dir)
            configure = configure.bake('-xplatform', 'android-clang')
            configure = configure.bake('-android-abis', arch.arch)
            configure = configure.bake('-extprefix', self.ctx.libs_dir)
            configure = configure.bake('-nomake', 'tests')
            configure = configure.bake('-nomake', 'examples')
            configure = configure.bake('-no-widgets')
            configure = configure.bake('-skip', ','.join(
                ['qtwebview','qtwebengine','qtquick3d',
                 'qtquick3dphysics']))

            # openssl
            openssl = Recipe.get_recipe('openssl', self.ctx)
            configure = configure.bake('-ssl', '-openssl-runtime')
            # configure = configure.bake('OPENSSL_INCDIR=' + join(openssl.get_build_dir(arch.arch), 'include'))
            configure = configure.bake('OPENSSL_INCLUDE_DIR=' + join(openssl.get_build_dir(arch.arch), 'include'))
            # configure = configure.bake('OPENSSL_LIBDIR=' + openssl.get_build_dir(arch.arch))
            configure = configure.bake('OPENSSL_LIBS=%s' % openssl.link_libs_flags().strip())

            for exclude in "quickcontrols2-fusion quickcontrols2-imagine quickcontrols2-universal".split(' '):
                configure = configure.bake('-no-feature-%s' % exclude)

            configure = configure.bake('--')
            configure = configure.bake('-DQT_NO_PACKAGE_VERSION_CHECK=TRUE')
            configure = configure.bake('-DQT_HOST_PATH=/usr/lib/qt6')

            for x in glob.glob('/usr/lib/x86_64-linux-gnu/cmake/*'):
                y = x.split('/')[-1]
                print(f'{x} {x!r} {y}')
                if y.startswith('Qt6'):
                    configure = configure.bake(f'-D{y}_DIR=/usr/lib/x86_64-linux-gnu/cmake/{y}')

            # configure = configure.bake('-DQt6HostInfo_DIR=/usr/lib/x86_64-linux-gnu/cmake/Qt6HostInfo')
            # configure = configure.bake('-DQt6CoreTools_DIR=/usr/lib/x86_64-linux-gnu/cmake/Qt6CoreTools')
            # configure = configure.bake('-DQt6WidgetsTools_DIR=/usr/lib/x86_64-linux-gnu/cmake/Qt6WidgetsTools')
            # configure = configure.bake('-DQt6GuiTools_DIR=/usr/lib/x86_64-linux-gnu/cmake/Qt6GuiTools')
            # configure = configure.bake('-DQt6BuildInternals_DIR=/usr/lib/x86_64-linux-gnu/cmake/Qt6BuildInternals')
            configure = configure.bake('-DQt6AndroidMacros_DIR=%s' % 'qtbase/src/corelib/Qt6AndroidMacros.cmake')
            configure = configure.bake('-DQT_ADDITIONAL_PACKAGES_PREFIX_PATH=/usr/lib/x86_64-linux-gnu')
            configure = configure.bake('-DCMAKE_PREFIX_PATH=/usr/lib/x86_64-linux-gnu/cmake')
            # configure = configure.bake('-DCMAKE_MODULE_PATH=/usr/lib/x86_64-linux-gnu/cmake')
            configure = configure.bake('--debug-find-pkg=WrapOpenGL')

            info(str(configure))

            shprint(configure, _tail=50, _critical=True)

            shprint(sh.make, '-j' + str(cpu_count()), _critical=True )
            shprint(sh.make, '-j' + str(cpu_count()), 'install', _critical=True )


    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        info('Copying Qt5 java class to classes build dir')
        # TODO: neatly filter *.java and *.aidl
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.cp, '-a', join('qtbase', 'src', 'android', 'java', 'src', 'org'), self.ctx.javaclass_dir)
            shprint(sh.cp, '-a', join('qtbase', 'src', 'android', 'java', 'src', 'org'), self.ctx.aidl_dir)

recipe = Qt6Recipe()
