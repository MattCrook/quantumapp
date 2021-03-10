const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
// outputPath is place where your want to save files
// Webpack uses `publicPath` to determine where the app is being served from.
module.exports = {
  mode: "development",
  // context: path.resolve(__dirname, "quantumadminapp/"),
  // context: __dirname,
  // entry: "./quantumadminapp/src/index.js",
  // entry: "./src/index.js",
  entry: {
    main: path.resolve(__dirname, 'quantumadminapp/src/index.js'),
  },
  output: {
    pathinfo: true,
    path: path.resolve(__dirname, "quantumadminapp/static"),
    filename: "js/[name].js",
    // filename: "js/bundle.js",
    chunkFilename: "js/[name].chunk.js",
    // clean: true,
    // publicPath: "static/app/",
    publicPath: "/static/",
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    modules: [
        path.resolve(__dirname, 'quantumadminapp/src'),
        path.resolve(__dirname, 'node_modules'),
    ],
  },
  // resolve: {
  //   alias: {
  //     src: path.resolve(__dirname, "./src"),
  //   },
  // },
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
        ],
      },
      // {
      //   test: /\.html$/,
      //   use: [
      //     {
      //       loader: "html-loader",
      //       options: {
      //         minimize: true,
      //       },
      //     },
      //   ],
      // },
      {
        test: /\.txt$/i,
        use: "raw-loader",
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        // type: "asset",
        exclude: /node_modules/,
        use: [
          {
            loader: "url-loader",
            options: {
              limit: 8192,
              name: "images/[name].[ext]",
            },
          },
        ],
      },
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        // type: "asset",
        exclude: /node_modules/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "images/[name].[ext]",
              // name: 'media/[name].[hash:8].[ext]',
              // path: path.resolve(__dirname, "static/"),
            },
          },
        ],
      },
    ],
  },
};

// resolve: { extensions: ["*", ".js", ".jsx"] },
// output: {
//   path: path.resolve("./quantumadminapp/static/app/"),
//   filename: "[name].js", // Emit app.js by capturing entry name
//   clean: true,
//   publicPath: "static/app/",
// },

// {
//   loader: "resolve-url-loader",
//   options: {
//     sourceMap: true,
//   },
// },
// ],
