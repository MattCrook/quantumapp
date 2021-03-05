const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: { app: ".src/index.js" }, // Start bundling
  output: {
    path: path.join(__dirname, "dist"), // Output to dist directory
    filename: "[name].js", // Emit app.js by capturing entry name
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        // output: {
        //   path: path.resolve(__dirname, "dist/"),
        //   publicPath: "",
        //   use: {
        //     loader: "babel-loader",
        //   },
        // },
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
        test: /\.(png|jpg|gif)$/i,
        use: [
          {
            loader: "file-loader",
            options: {
              path: path.resolve(__dirname, "dist/"),
              // path: "/static",
              // outputPath: "",
              // publicPath: "/static",
              name: "[path][name].[ext]",
            },
          },
        ],
      },
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
