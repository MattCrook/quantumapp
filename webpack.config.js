const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
// outputPath is place where your want to save files
// publicPath is what url you have in js, css and etc files.
module.exports = {
  mode: "development",
  context: path.resolve(__dirname, "quantumadminapp/"),
  entry: "./src/index.js",
  output: {
    pathinfo: true,
    path: path.resolve(__dirname, "quantumadminapp/static"),
    // filename: "[name].js", // Emit app.js by capturing entry name
    filename: "js/bundle.js",
    chunkFilename: 'js/[name].chunk.js',
    // clean: true,
    // publicPath: "static/app/",
    publicPath: "static/",
  },
  resolve: {
    alias: {
      src: path.resolve(__dirname, "./src"),
    },
  },
  devtool: "inline-source-map",
  devServer: {
    contentBase: path.join(__dirname, "dist/"),
    port: 8080,
    publicPath: "http://localhost:8080/dist/",
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: "Quantum Coasters Admin",
    }),
  ],
  // resolve: { extensions: ["*", ".js", ".jsx"] },
  // output: {
  //   path: path.resolve("./quantumadminapp/static/app/"),
  //   filename: "[name].js", // Emit app.js by capturing entry name
  //   clean: true,
  //   publicPath: "static/app/",
  // },
  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({
      path: __dirname,
      filename: "./webpack-stats.json",
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
        test: /\.html$/,
        use: [
          {
            loader: "html-loader",
            options: {
              minimize: true,
            },
          },
        ],
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
          // {
          //   loader: "resolve-url-loader",
          //   options: {
          //     sourceMap: true,
          //   },
          // },
        ],
      },
      {
        // test: /\.(gif|png|jpe?g|svg)$/i,
        // type: 'asset/resource',
        test: /\.(png|jp(e*)g|svg)$/,
        exclude: /node_modules/,
        use: [
          {
            loader: "url-loader",
            options: {
              limit: 8000,
              name: 'media/[name].[hash:8].[ext]',
              // name: "assets/[name].[md5:hash:hex:8].[ext]",
              // name: "media/[hash]-[name].[ext]",
              // encoding: "utf8",
            },
          },
        ],
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        exclude: /node_modules/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: 'media/[name].[hash:8].[ext]',
              // name: "assets/[name].[md5:hash:hex:8].[ext]",
              // name: "media/[hash]-[name].[ext]",
              // path: path.resolve(__dirname, "images"),
              // path: path.join(__dirname, "static", "images"),
              // outputPath: ASSETS.images,
              // publicPath: ASSETS.static,
              // outputPath: "images",
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
