const path = require("path");
const webpack = require("webpack");
// const HtmlWebpackPlugin = require('html-webpack-plugin');
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

// module.exports = {
//   entry: { app: "./index.js" }, // Start bundling
//   output: {
//     path: path.join(__dirname, "dist/"), // Output to dist directory
//     filename: "[name].js", // Emit app.js by capturing entry name
//   },

module.exports = {
  entry: ".src/index.js",
  mode: "development",
  //   output: {
  //   path: path.join(__dirname, "dist/"), // Output to dist directory
  //   filename: "[name].js", // Emit app.js by capturing entry name
  // },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/env"],
          },
        },
      },
      {
        test: /\.css$/i,
        exclude: /node_modules/,
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
        use: [
          // {
          //   loader: "image-webpack-loader",
          //   options: {
          //     mozjpeg: {
          //       progressive: true,
          //       quality: 65,
          //     },

          //     optipng: {
          //       enabled: false,
          //     },
          //     pngquant: {
          //       quality: [0.65, 0.9],
          //       speed: 4,
          //     },
          //     gifsicle: {
          //       interlaced: false,
          //     },

          //     webp: {
          //       quality: 75,
          //     },
          //   },
          // },
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "media/",
              publicPath: "media/",
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
      {
        test: /\.svg$/i,
        use: [
          {
            loader: "url-loader",
            options: {
              encoding: "utf8",
            },
          },
        ],
      },
      {
        test: /\.txt$/i,
        use: "raw-loader",
      },
    ],
  },
};
