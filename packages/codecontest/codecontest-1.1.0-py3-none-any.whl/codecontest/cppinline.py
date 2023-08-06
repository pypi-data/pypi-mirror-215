import json
import subprocess
import argparse
import sys
import codecontest as cc
import os
from collections import deque

def inline_and_compact(source_file):
    str_ast, concat_file = cc.cpp_ast(source_file)
    json_ast = json.loads(str_ast)
    lines = None
    with open(concat_file, 'r') as f:
        lines = f.readlines()
    
    decls = extract_decl(DeclNode(json_ast[0], lines=lines))
    used_decls = mark_used(main=DeclNode(json_ast[0]['inner'][-1], lines=lines), decls=decls)

    decls = sorted(list(decls.values()), key=lambda decl: decl.line_s)
    used_decls = sorted(list(used_decls), key=lambda decl: decl.line_s)

    # for x in decls: 
    #     print(x)
    # print('--------------------------')
    # for x in used_decls: print(x)

    print('#include <bits/stdc++.h>')
    print('using namespace std;')
    print()
    for idx, seg in enumerate(used_decls):
        if idx > 0 and len(seg.namespaces) > len(used_decls[idx - 1].namespaces):
            print(f'namespace {seg.namespaces[-1]} ' + '{')
        for i in range(seg.line_s - 1, seg.line_t - 1):
            print(lines[i], end='')
        if idx > 0 and len(seg.namespaces) < len(used_decls[idx - 1].namespaces):
            print('}')
        print()

def extract_decl(cur, namespaces=[]):
    maybes = {}
    # print(cur)
    if cur.is_namespacedecl():
        # cur.namespaces = list(namespaces) #deepcopy
        # maybes[cur] = cur
        
        namespaces.append(cur.name)
        for chd in cur.children():
            maybes.update(extract_decl(chd, namespaces))
        namespaces.pop()
        
    elif (False 
        or cur.is_vardecl() 
        or cur.is_funcdecl() 
        or cur.is_classdecl() 
        or cur.is_typealiasdecl()
    ):
        cur.namespaces = list(namespaces) #deepcopy
        maybes[cur] = cur
    return maybes

def mark_used(main, decls={}):
    que = deque()
    que.append(main)
    visited = set()
    used_segs = []
    while len(que) > 0:
        cur = decls[que.popleft()]
        used_segs.append(cur)
        visited.add(cur)
        for dep in cur.dependences():
            if dep not in visited and dep in decls:
                que.append(dep) #resolve to decl
    return used_segs


class DeclNode:
    def __init__(self, json_node, lines=None):
        self.json_node = json_node
        self.kind = json_node.get('kind', None)
        self.name = json_node.get('name', None)
        self.line_s, self.line_t = self.get_range() 
        self.namespaces = None
        self.used = False
        self.lines = lines
        self.id = None

    def get_range(self):
        try:
            line_s = self.json_node['loc']['line']
            line_s = self.json_node['range']['begin'].get('line', line_s)
            line_t = self.json_node['range']['end'].get('line', line_s) + 1
        except Exception as e:
            line_s, line_t = None, None
        return line_s, line_t

    def get_id(self):
        if self.id is not None:
            return self.id
        id = None
        if self.is_vardecl():
            id = self.json_node['id']
        elif self.is_varcall():
            id = self.json_node['referencedDecl']['id']
        elif self.is_funcdecl():
            id = self.json_node['id']
        elif self.is_funccall():
            id = self.json_node['referencedDecl']['id']
        elif self.is_classdecl():
            id = (self.namespaces, self.name)
        elif self.is_classcall():
            if self.namespaces is None:
                self.namespaces = self.json_node['type']['desugaredQualType'].split('::')[:-1]
                name = self.json_node['type']['qualType']
                self.name = name
                if '<' in name:
                    self.name = name[:name.find('<')]
            id = (self.namespaces, self.name)
        elif self.is_typealiasdecl():
            id = self.json_node['id']
        elif self.is_typealiascall():
            id = self.json_node['typeAliasDeclId']
        elif self.is_namespacedecl(): #todo
            id = self.json_node['id']
        else:
            raise Exception(f'cannot get_id of {self.json_node}!')
            # pass
        self.id = id
        return id
        
    def __eq__(self, other: object) -> bool:
        return self.get_id() == other.get_id()
    def __hash__(self) -> int:
        return hash(str(self.get_id()))

    def is_vardecl(self): return self.kind == 'VarDecl'
    def is_varcall(self): return self.kind == 'DeclRefExpr' and self.json_node['referencedDecl']['kind'] == 'VarDecl'
    def is_funcdecl(self): return self.kind in ('FunctionTemplateDecl', 'FunctionDecl')
    def is_funccall(self): return self.kind == 'DeclRefExpr' and self.json_node['referencedDecl']['kind'] == 'FunctionDecl'
    def is_classdecl(self): return self.kind in ('ClassTemplateDecl', 'CXXRecordDecl')
    def is_classcall(self): return self.kind in ('CXXConstructExpr',) #todo
    # def is_classbase(self): return 'access' in self.json_node and 'writtenAccess' in self.json_node
    def is_typealiasdecl(self): return self.kind in ('TypedefDecl', 'TypeAliasDecl')
    def is_typealiascall(self): return 'typeAliasDeclId' in self.json_node

    def is_namespacedecl(self): return self.kind == 'NamespaceDecl'
    
    def children(self):
        for chd in self.json_node.get('inner', []):
            yield DeclNode(chd, lines=self.lines)
        # typealias refer
        if 'type' in self.json_node:
            yield DeclNode(self.json_node['type'], lines=self.lines)

    def dependences(self):
        deps = []
        que = deque()
        que.append(self)
        while len(que) > 0:
            cur = que.popleft()
            if cur.is_varcall():
                deps.append(cur)
            elif cur.is_funccall():
                deps.append(cur)
            elif cur.is_classcall():
                deps.append(cur)
            elif cur.is_typealiascall():
                # print('typealiascall', cur)
                deps.append(cur)
            else:
                pass
            que.extend(cur.children())
        return deps
        
    def __str__(self) -> str:
        try:
            content = ''.join(self.lines[self.line_s - 1:self.line_t - 1])
        except Exception:
            content = None
        return str((self.get_id(), self.namespaces, self.name, self.line_s, self.line_t, content))
    def __repr__(self) -> str:
        return self.__str__()

# inline_and_compact('/tmp/inlined.cpp')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    args = parser.parse_args()
    inline_and_compact(args.source_file)