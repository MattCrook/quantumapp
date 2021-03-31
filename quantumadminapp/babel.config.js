module.exports = {
    presets: [
      [
        "@babel/preset-env",
        // {
        //   modules: false
        // }
      ],
      "@babel/preset-react"
    ],
    plugins: [
      "@babel/plugin-transform-runtime",
      "@babel/plugin-syntax-dynamic-import",
      "@babel/plugin-proposal-class-properties"
    ],
    env: {
      production: {
        only: ["src"],
        plugins: [
          [
            "transform-react-remove-prop-types",
            {
              removeImport: true
            }
          ],
          "@babel/plugin-transform-react-inline-elements",
          "@babel/plugin-transform-react-constant-elements"
        ]
      }
    }
  };



  // module.exports = {
  //   env: {
  //     test: {
  //       plugins: ['transform-class-properties'],
  //       presets: [
  //         '@babel/preset-env',
  //         '@babel/preset-react',
  //         '@babel/preset-typescript'
  //       ]
  //     }
  //   }
  // };
