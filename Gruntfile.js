module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
            dist: {
                files: {
                    'static/css/wedding.css' : 'static/scss/wedding.scss',
                    'static/css/cms.css' : 'static/scss/cms.scss'
                }
            }
        },
        watch: {
            css: {
                files: 'static/scss/**/*.scss',
                tasks: ['sass']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('default',['sass', 'watch']);
};