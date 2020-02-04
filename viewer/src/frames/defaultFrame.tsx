import * as React from "react";
import * as ReactDom from "react-dom";

/** 
 * [index]
 * +-----------+-----------+-----------+
 * |key 0      |key 1      |key 2      |
 * +-----------+-----------+-----------+ ...
 * |IndexInfo 0|IndexInfo 1|IndexInfo 2|
 * +-----------+-----------+-----------+ 
 * [contents]
 * +-----------+-----------+-----------+
 * |key 0      |key 1      |key 2      |
 * +-----------+-----------+-----------+ ...
 * |Content 0  |Content 1  |Content 2  |
 * +-----------+----------- +----------+ 
 * 
 * [tags]
 * +-------+------+------+
 * |Tag a  |Tag b |Tag c | ...
 * +-------+------+------+ 
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
  indicesInfo: Array<IndexInfo>;
  contents: Array<Content>;
  tags: Array<Tag>;
}

const dataCast = (fileNames: Array<string>,
                  texts: Array<string>,
                  histories: Array<string>,
                  loadedTags: any) // ?
                  : DefaultFrameProps => {

  const indicesInfo: Array<IndexInfo> = [];
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

    const content_tags: Array<string> = loadedTags[fileName];

    const content: Content = {
      "title": title,
      "text": text,
      "history": histories[idx],
      "tags": content_tags
    }

    indicesInfo.push(indexInfo);
    contents.push(content);

    const tagHolder: TagHolder = {};
    for (const tagName in loadedTags[fileName]) {
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
    "indicesInfo": indicesInfo,
    "contents": contents,
    "tags": tags
  }
}

const indexRender = (indicesInfo: Array<IndexInfo>) => {
}

const contentRender = (index: number, contents: Array<Content>) => {
}

const tagRender = (tags: Array<Tag>) => {
}