import * as React from "react";
import * as ReactDom from "react-dom";
const ReactMarkdown = require("react-markdown");

const setUp = () => {
  const build_config = require("../package.json");
  const markdown_content = require("../dummy-mark.md");
  console.log(build_config)
  console.log(markdown_content)
  return markdown_content 
}

const markdown_content = setUp();

ReactDom.render(
  <div>
    <ReactMarkdown source={markdown_content["default"]} />
  </div>,
  document.getElementById("demo")
);
