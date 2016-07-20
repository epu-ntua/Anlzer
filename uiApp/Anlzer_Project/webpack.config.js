/**
 * Created by DarkA_000 on 5/12/2016.
 */

var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: {
    'bundle': './anlzer/static/anlzer/js/app/modules/assets/index'
  }, 

  output: {
      path: path.resolve('./anlzer/static/anlzer/js/app/modules/assets/bundles/'),
      filename: "bundle.js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel'// to transform JSX into JS
      }
    ],
  },

  resolve: {
    modulesDirectories: ['node_modules', 'bower_components'],
    extensions: ['', '.js', '.jsx']
  },
}
