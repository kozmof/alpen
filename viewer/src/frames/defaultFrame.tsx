import * as React from "react";
import * as ReactDom from "react-dom";

/*
index
+-----------+-----------+-----------+-----------+-----------+-----------+
|key 0      |key 1      |key 2      |key 3      |key 4      |key 5      |
+-----------+-----------+-----------+-----------+-----------+-----------+ ...
|IndexInfo 0|IndexInfo 1|IndexInfo 2|IndexInfo 3|IndexInfo 4|IndexInfo 5|
+-----------+-----------+-----------+-----------+-----------+-----------+ 

contents
+---------+---------+---------+---------+---------+---------+
|key 0    |key 1    |key 2    |key 3    |key 4    |key 5    |
+---------+---------+---------+---------+---------+---------+ ...
|Content 0|Content 1|Content 2|Content 3|Content 4|Content 5|
+---------+---------+---------+---------+---------+---------+ 

tags
+-------+------+------+
|Tag a  |Tag b |Tag c | ...
+-------+------+------+ 
*/

type IndexInfo = {
  title: string;
  createdDate: string;
  revisionDate: string;
}

type Tag = {
  tag: string;
  keys: Array<number>;
}

type TagHolder = {
  [key: string]: Tag
}

type Content = {
  title: string;
  text: string;
  history: string;
  tags: Array<string>;
}

interface DefaultFrameProps {
  index: Array<IndexInfo>;
  contents: Array<Content>;
  tags: Array<Tag>;
}

const dataCast = (fileNames: Array<string>,
                  texts: Array<string>,
                  histories: Array<string>,
                  tag: any) // ?
                  : DefaultFrameProps => {

  const index: Array<IndexInfo> = [];
  const contents: Array<Content> = [];
  const tags: Array<Tag> = []

  for (const [idx, fileName] of fileNames.entries()) {
    const text: string = texts[idx];
    const title: string = text.split("\n")[0];
    const indexInfo: IndexInfo = {
      "title": title,
      "createdDate": "",
      "revisionDate": ""
    }

    const content_tags: Array<string> = tag[fileName];

    const content: Content = {
      "title": title,
      "text": text,
      "history": histories[idx],
      "tags": content_tags
    }

    index.push(indexInfo);
    contents.push(content);

    const tagHolder: TagHolder = {};
    for (const tagName in tag[fileName]) {
      if (tagName in tagHolder) {
          tagHolder[tagName].keys.push(idx)
        } else {
          tagHolder[tagName] = {
            "tag": tagName,
            "keys": [idx]
          }
        }
      }

    for (const tagName in tagHolder) {
        tags.push(tagHolder[tagName]);
    }
  }

  return {
    "index": index,
    "contents": contents,
    "tags": tags
  }
}