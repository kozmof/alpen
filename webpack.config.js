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
            { enforce: "pre", test: /\.js$/, loader: "source-map-loader" }
        ] 
    },

    externals: {
        "react": "React", 
        "react-dom": "ReactDOM"
    }
        
}
