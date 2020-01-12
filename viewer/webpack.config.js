module.exports = {
    entry: "./src/index.tsx",
    output: {
        filename: "bundle.js", 
        path: __dirname + "/dist"
    },

    mode: "development",

    devtool: "source-map",

    resolve: {
        extensions: [".ts", ".tsx", ".js", ".json"] 
    },

    module: {
        rules: [
            { test: /\.tsx?$/, loader: "ts-loader" }, 
            { test: /\.md$/i, loader: "raw-loader" }, 
            { test: /\.json$/, loader: "json-loader", type: "javascript/auto" }, 
            { enforce: "pre", test: /\.js$/, loader: "source-map-loader" }
        ]
    },

    externals: {
        "react": "React", 
        "react-dom": "ReactDOM"
    }
        
}
