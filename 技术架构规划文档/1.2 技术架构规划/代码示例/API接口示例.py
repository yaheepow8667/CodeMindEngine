# API接口示例

# 1. FastAPI后端接口定义示例（team.py）

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from starlette import status

from app import crud, schemas, models
from app.api import deps
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/", response_model=List[schemas.Team], summary="获取团队列表")
def read_teams(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    """
    获取当前用户所在的团队列表
    
    - **skip**: 分页跳过的条数
    - **limit**: 分页获取的条数
    - **name**: 团队名称搜索（可选）
    """
    teams = crud.team.get_teams(db, user_id=current_user.user_id, skip=skip, limit=limit, name=name)
    return teams

@router.post("/", response_model=schemas.Team, status_code=status.HTTP_201_CREATED, summary="创建团队")
def create_team(
    team_in: schemas.TeamCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    创建新团队
    
    - **name**: 团队名称（必填）
    - **description**: 团队描述（可选）
    """
    # 检查团队名称是否已存在
    existing_team = crud.team.get_team_by_name(db, name=team_in.name)
    if existing_team:
        raise HTTPException(status_code=400, detail="团队名称已存在")
    
    # 创建团队
    team = crud.team.create_team(db, team_in=team_in, created_by=current_user.user_id)
    
    # 将创建者添加为团队成员
    crud.team_member.create_team_member(
        db, 
        team_member_in=schemas.TeamMemberCreate(
            team_id=team.team_id, 
            user_id=current_user.user_id, 
            role="owner"
        )
    )
    
    return team

@router.get("/{team_id}", response_model=schemas.Team, summary="获取团队详情")
def read_team(
    team_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    获取指定团队的详情
    
    - **team_id**: 团队ID
    """
    team = crud.team.get_team_by_id(db, team_id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="团队不存在")
    
    # 检查用户是否为团队成员
    team_member = crud.team_member.get_team_member(db, team_id=team_id, user_id=current_user.user_id)
    if not team_member:
        raise HTTPException(status_code=403, detail="无权限访问该团队")
    
    return team

@router.put("/{team_id}", response_model=schemas.Team, summary="更新团队信息")
def update_team(
    team_id: int,
    team_in: schemas.TeamUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    更新团队信息
    
    - **team_id**: 团队ID
    - **name**: 团队名称（可选）
    - **description**: 团队描述（可选）
    """
    # 获取团队信息
    team = crud.team.get_team_by_id(db, team_id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="团队不存在")
    
    # 检查用户是否为团队所有者
    team_member = crud.team_member.get_team_member(db, team_id=team_id, user_id=current_user.user_id)
    if not team_member or team_member.role != "owner":
        raise HTTPException(status_code=403, detail="只有团队所有者可以更新团队信息")
    
    # 检查团队名称是否已存在
    if team_in.name and team_in.name != team.name:
        existing_team = crud.team.get_team_by_name(db, name=team_in.name)
        if existing_team:
            raise HTTPException(status_code=400, detail="团队名称已存在")
    
    # 更新团队信息
    team = crud.team.update_team(db, team=team, team_in=team_in)
    return team

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除团队")
def delete_team(
    team_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    删除指定团队
    
    - **team_id**: 团队ID
    """
    # 获取团队信息
    team = crud.team.get_team_by_id(db, team_id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="团队不存在")
    
    # 检查用户是否为团队所有者
    team_member = crud.team_member.get_team_member(db, team_id=team_id, user_id=current_user.user_id)
    if not team_member or team_member.role != "owner":
        raise HTTPException(status_code=403, detail="只有团队所有者可以删除团队")
    
    # 删除团队
    crud.team.delete_team(db, team_id=team_id)

# 2. 前端API调用示例（api/team.js）

/*
import request from '@/utils/request'

// 获取团队列表
export function getTeams(params) {
  return request({
    url: '/api/v1/teams',
    method: 'get',
    params
  })
}

// 获取团队详情
export function getTeamById(teamId) {
  return request({
    url: `/api/v1/teams/${teamId}`,
    method: 'get'
  })
}

// 创建团队
export function createTeam(data) {
  return request({
    url: '/api/v1/teams',
    method: 'post',
    data
  })
}

// 更新团队
export function updateTeam(teamId, data) {
  return request({
    url: `/api/v1/teams/${teamId}`,
    method: 'put',
    data
  })
}

// 删除团队
export function deleteTeam(teamId) {
  return request({
    url: `/api/v1/teams/${teamId}`,
    method: 'delete'
  })
}

// 获取团队成员
export function getTeamMembers(teamId, params) {
  return request({
    url: `/api/v1/teams/${teamId}/members`,
    method: 'get',
    params
  })
}

// 添加团队成员
export function addTeamMember(teamId, data) {
  return request({
    url: `/api/v1/teams/${teamId}/members`,
    method: 'post',
    data
  })
}

// 更新团队成员角色
export function updateTeamMemberRole(teamId, memberId, data) {
  return request({
    url: `/api/v1/teams/${teamId}/members/${memberId}`,
    method: 'put',
    data
  })
}

// 移除团队成员
export function removeTeamMember(teamId, memberId) {
  return request({
    url: `/api/v1/teams/${teamId}/members/${memberId}`,
    method: 'delete'
  })
}
*/
