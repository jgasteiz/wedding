module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        dev: 'static/src',
        build: 'static/build',

        sass: {
            dist: {
                files: {
                    '<%= dev %>/css/wedding.css' : '<%= dev %>/scss/wedding.scss',
                    '<%= dev %>/css/cms.css' : '<%= dev %>/scss/cms.scss'
                }
            }
        },
        watch: {
            css: {
                files: '<%= dev %>/scss/**/*.scss',
                tasks: ['sass']
            }
        },

        cssmin: {
            options: {
                shorthandCompacting: false,
                roundingPrecision: -1
            },
            public: {
                files: {
                    '<%= build %>/css/wedding.min.css': [
                        '<%= dev %>/css/wedding.css'
                    ]
                }
            },
            cms: {
                files: {
                    '<%= build %>/css/cms.min.css': [
                        '<%= dev %>/css/cms.css'
                    ]
                }
            }
        },
        copy: {
            img: {
                files: [
                    {
                        expand: true,
                        dest: '<%= build %>/img/',
                        src: ['**'],
                        cwd: '<%= dev %>/img'
                    }
                ]
            },
            js: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        src: '<%= dev %>/libs/picturefill/dist/picturefill.min.js',
                        dest: '<%= build %>/js/'
                    }
                ]
            }
        },
        uglify: {
            public: {
                files: {
                    '<%= build %>/js/wedding.min.js': [
                        '<%= dev %>/libs/jquery/dist/jquery.js',
                        '<%= dev %>/js/wedding.js'
                    ]
                }
            },
            //cms: {
            //    files: {
            //        '<%= build %>/js/cms.min.js': [
            //            '<%= dev %>/libs/jquery/dist/jquery.js',
            //            '<%= dev %>/libs/bootstrap-datetimepicker/src/js/bootstrap-datetimepicker.js',
            //            '<%= dev %>/libs/trumbowyg/dist/trumbowyg.js',
            //            '<%= dev %>/js/cms/alert-dismiss.js',
            //            '<%= dev %>/js/cms/datetimepicker-setup.js',
            //            '<%= dev %>/js/cms/trumbowyg-setup.js',
            //            '<%= dev %>/js/components/preview-image.js'
            //        ]
            //    }
            //}
        }
    });

    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-cssmin');

    grunt.registerTask('default',['sass', 'watch']);

    grunt.registerTask('build', ['uglify', 'sass', 'cssmin', 'copy']);
};