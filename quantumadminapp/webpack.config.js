const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserWebpackPlugin = require("terser-webpack-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
// outputPath is place where your want to save files
// Webpack uses `publicPath` to determine where the app is being served from.
// module.exports = {
module.exports = function (_env, argv) {
  const isProduction = argv.mode === "production";
  const isDevelopment = !isProduction;
  return {
    mode: "development",
    entry: "./src/index.js",
    output: {
      pathinfo: true,
      path: path.resolve(__dirname, "./static/quantumadmin"),
      filename: "js/[name].js",
      chunkFilename: "js/[name].chunk.js",
      publicPath: "/static/quantumadmin",
    },
    devtool: isDevelopment && "cheap-module-source-map",
    devServer: {
      contentBase: path.join(__dirname, "dist/"),
      port: 3001,
      publicPath: "http://localhost:3001/dist/",
      compress: true,
      historyApiFallback: true,
      open: true,
      overlay: true,
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
            options: {
              // presets: ["@babel/env"],
              cacheDirectory: true,
              cacheCompression: false,
              envName: isProduction ? "production" : "development",
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
        {
          test: /\.(png|jpg|gif)$/i,
          // type: "asset",
          use: [
            {
              loader: "url-loader",
              options: {
                limit: 8192,
                name: "/images/[name].[ext]",
                // name: "images/[name].[hash:8].[ext]",
              },
            },
          ],
        },
        {
          test: /\.txt$/i,
          use: "raw-loader",
        },
        {
          test: /\.svg$/,
          use: ["@svgr/webpack"],
        },
        {
          test: /\.(eot|otf|ttf|woff|woff2)$/,
          use: [
            {
              loader: require.resolve("file-loader"),
              options: {
                name: "/images/[name].[ext]",
                // name: "images/[name].[hash:8].[ext]",
              },
            },
          ],
        },
      ],
    },
    // optimization: {
    //   minimize: true,
    // },
    optimization: {
      minimize: isProduction,
      minimizer: [
        new TerserWebpackPlugin({
          terserOptions: {
            compress: {
              comparisons: false,
            },
            mangle: {
              safari10: true,
            },
            output: {
              comments: false,
              ascii_only: true,
            },
            warnings: false,
          },
        }),
        new OptimizeCssAssetsPlugin(),
      ],
    },
    resolve: {
      extensions: ["*", ".js", ".jsx"],
      // modules: [
      //   path.resolve(__dirname, "src"),
      //   path.resolve(__dirname, "node_modules"),
      // ],
    },
    plugins: [
      new CleanWebpackPlugin(),
      new BundleTracker({
        path: __dirname,
        filename: "./webpack-stats.json",
      }),
      new webpack.DefinePlugin({
        "process.env.NODE_ENV": JSON.stringify(
          isProduction ? "production" : "development"
        ),
      }),
      new HtmlWebpackPlugin({
        // title: "Quantum Coasters Admin",
        // template: path.resolve(__dirname, "public/index.html"),
        template: path.resolve(__dirname, "templates/index.html"),
        inject: true,
      }),
    ].filter(Boolean),
  };
};

// ],
// plugins: [
//   new CleanWebpackPlugin(),
//   new BundleTracker({
//     path: __dirname,
//     filename: "./webpack-stats.json",
//   }),

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
