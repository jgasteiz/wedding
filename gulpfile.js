'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    gconcat = require('gulp-concat'),
    cssmin = require('gulp-cssmin');

gulp.task('sass', function () {
    gulp.src('./static/src/scss/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./static/src/css'));
});

gulp.task('cssmin', function () {
    gulp.src([
            './static/src/css/cms.css',
            './static/src/libs/bootstrap/dist/css/bootstrap.css',
            './static/src/libs/bootstrap/dist/css/bootstrap-theme.css'
        ])
        .pipe(gconcat('cms.min.css'))
        .pipe(cssmin())
        .pipe(gulp.dest('./static/build/css'));

    gulp.src('./static/src/css/wedding.css')
        .pipe(gconcat('wedding.min.css'))
        .pipe(cssmin())
        .pipe(gulp.dest('./static/build/css'));
});

gulp.task('watch', function () {
    gulp.watch('./static/src/scss/*.scss', function () {
        gulp.start('sass');
    });
});

gulp.task('uglify', function() {
    // Uglify public js
    gulp.src(['./static/src/libs/jquery/dist/jquery.js', './static/src/js/wedding.js'])
        .pipe(gconcat('wedding.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./static/build/js'));
});

gulp.task('copy', function() {
    // Copy images
    gulp.src('./static/src/img/**/*')
        .pipe(gulp.dest('./static/build/img'));

    // Copy fonts
    gulp.src('./static/src/libs/bootstrap/dist/fonts/**/*')
        .pipe(gulp.dest('./static/build/fonts'));

    // Copy js files
    gulp.src([
        './static/src/libs/picturefill/dist/picturefill.min.js',
        './static/src/js/analytics.js',
        './static/src/libs/jquery/dist/jquery.min.js',
        './static/src/libs/bootstrap/dist/js/bootstrap.min.js',
        './static/src/libs/ace-builds/src-min-noconflict/ace.js',
        './static/src/libs/ace-builds/src-min-noconflict/theme-monokai.js',
        './static/src/libs/ace-builds/src-min-noconflict/mode-html.js',
        './static/src/js/editor.js',
        './static/src/js/invitees.js'])
        .pipe(gulp.dest('./static/build/js'));
});

gulp.task('default', ['sass', 'watch']);

gulp.task('build', ['uglify', 'sass', 'cssmin', 'copy']);
