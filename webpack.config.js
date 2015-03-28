var webpack = require("webpack");
var version = require('./package.json').version;
var fs = require('fs');
var path = require('path');




var bowerPath = path.resolve(path.join(__dirname, "bower_components"));
var webpackDirectories = [bowerPath, path.resolve(path.join(__dirname, 'web', 'js'))];

// iterate bower modules and add all igbtoolbox modules to webpack path
var mds = fs.readdirSync(bowerPath);
mds.forEach(function(md) {
  // read bower.json
  var bowerfile = path.join(bowerPath, md, "bower.json");
  if(fs.existsSync(bowerfile)) {
    var bv = require(bowerfile);
    if(!bv || !bv.moduleType || bv.moduleType.indexOf("igbtoolbox") == -1) {
      return;
    }

    // add web/js dir if exists
    var mp = path.resolve(path.join(bowerPath, md, "web", "js"));
    if(fs.existsSync(mp)) {
      console.info("Adding module js directory: " + mp);
      webpackDirectories.push(mp);
    }
    var mp = path.resolve(path.join(bowerPath, md, "web", "css"));
    if(fs.existsSync(mp)) {
      console.info("Adding module css directory: " + mp);
      webpackDirectories.push(mp);
    }
  }
});


module.exports = {
  entry: './web/js/igbtoolbox/bootstrap',
  output: {
    path: __dirname + '/web/js/build/',
    filename: 'igbtoolbox.js',
    sourceMapFilename: '[file].map',
    publicPath: "/static/common/js/build/"
  },
  resolve: {
    root: webpackDirectories,
    alias: {
      jquery: "jquery/dist/jquery",
      'jquery-ui': "jquery-ui/ui",
      moment: 'momentjs/moment.js',
      // react: 'react/react-with-addons',
      sockjs: 'sockjs/sockjs',
      numeral: 'numeraljs',
      immutable: 'immutable/dist/immutable.js',
      rx: 'rxjs/dist/rx.all'
    },
    extensions: ['', '.js', '.jsx'],
  },
  devtool: "#eval",
  resolveLoader: {
    root:  path.join(__dirname, "node_modules")
  },
  module: {
    loaders: [
      {
        //tell webpack to use jsx-loader for all *.jsx files
        test: /\.jsx$/,
        //loader: 'jsx-loader?insertPragma=React.DOM&harmony'
        loader: 'jsx-loader'
      },
      { test: /\.css$/, loader: "style-loader!css-loader" },
      // the optional 'selfContained' transformer tells babel to require the runtime instead of inlining it.
      {test: /\/eve.+?\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader?modules=amd&optional=selfContained'}
    ]
  },
  externals: {
    //don't bundle the 'react' npm package with our bundle.js
    //but get it from a global 'React' variable
    //'react': 'React'
  }
};
