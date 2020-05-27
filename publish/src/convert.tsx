type Hash = string;

/**
 * title/doc-1
 *      /doc-2
 * tag/tag-1
 *    /tag-2
 * domain/domain-1
 *       /domain-2
 */

type PayloadTitle = {
  [hash: string]: {
    title: string;
    tag: string[];
    domain: string[];
    publishDate: string;
    reviseDate: string;
    relPath: string;
  }
}

type PayloadPage = {
  fileName: string;
  doc: string;
  history: Array<{diff: string; timestmap: string;}>;
  tag: string[];
  domain: string[];
  publishDate: string;
  reviseDate: string;
}

type PayloadTag = {
    [tagName: string]: Hash[];
  }

type PayloadDomain = {
    [domainName: string]: Hash[];
}