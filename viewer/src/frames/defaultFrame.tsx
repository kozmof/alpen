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
  created_date: string;
  revision_date: string;
}

type Tag = {
  tag: string;
  keys: Array<number>;
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