import * as React from "react";
import * as ReactDom from "react-dom";

/*
index
+-------+-------+-------+-------+-------+-------+
|key 0  |key 1  |key 2  |key 3  |key 4  |key 5  |
+-------+-------+-------+-------+-------+-------+ ...
|title 0|title 1|title 2|title 3|title 4|title 5|
+-------+-------+-------+-------+-------+-------+ 

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
  index: Array<string>;
  contents: Array<Content>;
  tags: Array<Tag>;
}