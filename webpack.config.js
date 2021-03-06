const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require('html-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')


const NAMES = {
  images: "images",
  assets: "assets",
  static: "static",
};

const ASSETS = {
  images: path.join(NAMES.assets, NAMES.images),
  static: path.join(NAMES.static, NAMES.assets, NAMES.images),
};



module.exports = {
  mode: 'development',
  entry: { quantumadminapp: "./quantumadminapp/src/index.js" },
  devtool: 'inline-source-map',
  devServer: {
    contentBase: path.join(__dirname, "dist/"),
    port: 8080,
    publicPath: "http://localhost:8080/dist/",
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Quantum Coasters Admin',
    }),
  ],
  resolve: { extensions: ["*", ".js", ".jsx"] },
  output: {
    path: path.resolve('./quantumadminapp/static/app/'),
    filename: "[name].js", // Emit app.js by capturing entry name
    // path: path.join(__dirname, "static"), // Output to dist directory
    clean: true,
    publicPath: "static/app/",
  },
  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({
      path: __dirname,
      filename: './webpack-stats.json',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/env"],
            cacheDirectory: true,
          },
        },
      },
      {
        test: /\.css$/i,
        use: [
          {
            loader: "style-loader",
          },
          {
            loader: "css-loader",
            options: {
              sourceMap: true,
              url: true,
            },
          },
          {
            loader: "resolve-url-loader",
            options: {
              sourceMap: true,
            },
          },
        ],
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        type: 'asset/resource',
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              // path: path.join(__dirname, "static", "images"),
              // outputPath: ASSETS.images,
              // publicPath: ASSETS.static,
              // outputPath: "images",
              // publicPath: "images",


            },
          },
          {
            loader: "url-loader",
            options: {
              encoding: "utf8",
            },
          },
        ],
      },

      // {
      //   test: /\.(png|jpg|gif)$/i,
      //   use: [
      //     {
      //       loader: "file-loader",
      //       options: {
      //         // path: path.resolve(__dirname, "dist/"),
      //         // path: "/static/media",
      //         outputPath: ASSETS.images,
      //         // publicPath: "/static/media",
      //         name: "[path][name].[ext]",
      //       },
      //     },
      //   ],
      // },
      // {
      //   test: /\.(png|jpe?g|gif)$/i,
      //   use: [
      //     {
      //       loader: "file-loader",
      //       query:{
      //         outputPath: './media/',
      //         name: '[name].[ext]?[hash]'
      //     }
      //     },
      //   ],
      // },
      // {
      //   test: /\.svg$/i,
      //   use: [
      //     {
      //       loader: "url-loader",
      //       options: {
      //         encoding: "utf8",
      //       },
      //     },
      //   ],
      // },
      {
        test: /\.txt$/i,
        use: "raw-loader",
      },
    ],
  },
};








// const MiniCssExtractPlugin = require("mini-css-extract-plugin");
// const ImageminPlugin = require('imagemin-webpack-plugin').default;
// const CopyPlugin = require('copy-webpack-plugin');

// const PATHS = {
//   // when using __dirname, resolve and join gives same result,
//   // because __dirname is absolute path to directory of this file.
//   // OK to use no slashes,
//   // both resolve and join adds platform-specific separators by default
//   src: path.resolve(__dirname, "src"),
//   dist: path.resolve(__dirname, "dist"),
//   build: path.resolve(__dirname, "build"),
//   test: path.resolve(__dirname, "test"),
// };

// const NAMES = {
//   // JS FILES
//   index: "index",
//   print: "print",
//   // Chrome Extension Development
//   popup: "popup",
//   options: "options",
//   background: "background",
//   contentScript: "contentScript",

//   // FOLDERS
//   assets: "assets",
//   utilities: "utilities",
//   images: "images",
//   fonts: "fonts",
//   include: "include",
// };

// const FILE_PATHS = {
//   // JS
//   indexJs: `${path.join(PATHS.src, NAMES.index)}.js`,
//   printJs: `${path.join(PATHS.src, NAMES.print)}.js`,
//   // Chrome Extension Development
//   popupJs: `${path.join(PATHS.src, NAMES.popup)}.js`,
//   optionsJs: `${path.join(PATHS.src, NAMES.options)}.js`,
//   backgroundJs: `${path.join(PATHS.src, NAMES.background)}.js`,
//   contentScriptJs: `${path.join(PATHS.src, NAMES.include, NAMES.contentScript)}.js`,

//   // HTML
//   indexHtml: `${path.join(PATHS.src, NAMES.index)}.html`,
//   printHtml: `${path.join(PATHS.src, NAMES.print)}.html`,
//   // Chrome Extension Development
//   popupHtml: `${path.join(PATHS.src, NAMES.popup)}.html`,
//   optionsHtml: `${path.join(PATHS.src, NAMES.options)}.html`,
//   backgroundHtml: `${path.join(PATHS.src, NAMES.background)}.html`,
// };

// const ASSETS = {
//   images: path.join(NAMES.assets, NAMES.images),
//   fonts: path.join(NAMES.assets, NAMES.fonts),
// };
