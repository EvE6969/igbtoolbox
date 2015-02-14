module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    concat: {
      requires: {
        src: [
        'web/js/igbtoolbox/tools-loader.head.js',
        'bower_components/*/web/js/require.js',
        'web/js/igbtoolbox/tools-loader.tail.js'],
        dest: 'web/js/igbtoolbox/tools-loader.js'
      },
    },

    cssmin: {
      target: {
        files: {
          'web/css/igbtoolbox.min.css': [
            'bower_components/jquery-ui/themes/ui-darkness/jquery-ui.css',
            'web/css/media-debug.css',
            'web/css/site-debug.css',
            'web/css/reset-min.css',
            'web/css/theme/custom.css'
          ]
        }
      }
    }

  });


  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-cssmin');

};
