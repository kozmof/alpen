type Hash = string;

type JSONPayload = {
  titles: {
    [title: string]: Hash;
  }
  pages: {
    [Hash: string]: {
      fileName: string;
      doc: string;
      history: Array<{diff: string; timestmap: string;}>;
      tag: string[];
      domain: string[];
      publishDate: string;
      reviseDate: string;
    }
  }
  tags: {
    [tagName: string]: Hash[];
  }
  domain: {
    [domainName: string]: Hash[];
  }
}